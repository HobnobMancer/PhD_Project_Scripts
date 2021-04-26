#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:
# Emma E. M. Hobbs
#
# Contact
# eemh1@st-andrews.ac.uk
#
# Emma E. M. Hobbs,
# Biomolecular Sciences Building,
# University of St Andrews,
# North Haugh Campus,
# St Andrews,
# KY16 9ST
# Scotland,
# UK
#
# The MIT License


import random

import pandas as pd

from tqdm import tqdm

from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.utils import resample


def retrieve_ground_truths(classifications_df, cazy_dict):
    """Retrieve dict of ground truth CAZyme/non-CAZyme predictions. {accession: {tool: prediction}}

    :param classifications_df: pandas dataframe of prediction tool CAZyme/non-CAZyme classifications
    for each protein. Each protein is one row, each prediction tool is one column.

    Return dict of ground truths {accession: {"CAZy": prediction(0/1)}}"""
    cazy_annotation = []
    # tool_predictions = clasifications_df

    protein_accessions = classifications_df.index
    for protein_accession in protein_accessions:
        try:
            cazy_dict[protein_accession]
            cazyme_classification = 1
        except KeyError:
            cazyme_classification = 0

        cazy_annotation.append(cazyme_classification)

    classifications_df["CAZy"] = cazy_annotation  # add known CAZy annotations into new column of df

    return classifications_df


def get_prediction_classifications(tool_predictions, prediction_tool, classifications):
    """Retrieve dict of CAZyme prediction tool predictions of CAZyme/non-CAZyme classification.

    :param tool_predictions: list of CazymeProteinPrediction instances
    :param prediction_tool: str, name of the prediction tool being passed
    :param classifications: dict of CAZyme/non-CAZyme predicted classifications

    Return list of CAZyme/non-CAZymes classifications, written in long form to match TidyData
    requirements and recommendations in R.
    """
    # classifications  # [protien_accession, tool, cazyme classification]
    if (prediction_tool == "eCAMI") or (prediction_tool == "CUPP"):
        for prediction in tqdm(tool_predictions, desc=f"Retreiving {prediction_tool} predictions"):
            accession = prediction.protein_accession.split(" ")[0]
            classifications.append([accession, prediction_tool, prediction.cazyme_classification])
        return classifications

    for prediction in tqdm(tool_predictions, desc=f"Retreiving {prediction_tool} predictions"):
        classifications.append(
            [
                prediction.protein_accession,
                prediction_tool,
                prediction.cazyme_classification
            ],
        )
    return classifications


def build_classification_df(classifications):
    """Build dataframe of classifications. Unique protein per row, unqiue tool per column.

    :param classifications: dict of known and predicted classificaitons.

    Return pandas dataframe.
    """
    classification_dict = {}  # { protein_acession : {prediction_tool : [all_classiciations]} }
    for c in classifications:
        protein_accession = c[0]
        prediciton_tool = c[1]
        cazyme_classification = c[2]
        try:
            classification_dict[protein_accession]

            try:
                classification_dict[protein_accession][prediciton_tool]
                classification_dict[protein_accession][prediciton_tool].append(
                    cazyme_classification
                )
            except KeyError:
                classification_dict[protein_accession][prediciton_tool] = [cazyme_classification]

        except KeyError:
            classification_dict[protein_accession] = {}
            classification_dict[protein_accession][prediciton_tool] = [cazyme_classification]

    # build a series of lists
    data = []  # [Protein_accession, dbcan, hmmer, hotpep, diamond, cupp, ecami]
    for protein_accession in classification_dict:
        for i in range(len(classification_dict[protein_accession]["dbCAN"])):
            new_data = [protein_accession]
            for tool in ["dbCAN", "HMMER", "Hotpep", "DIAMOND", "CUPP", "eCAMI"]:
                new_data.append(classification_dict[protein_accession][tool][i])
            data.append(new_data)

    df = pd.DataFrame(
        data,
        columns=[
            "Protein_accession",
            "dbCAN",
            "HMMER",
            "Hotpep",
            "DIAMOND",
            "CUPP",
            "eCAMI",
        ],
    )
    df = df.set_index("Protein_accession")

    return df


def evaluate_binary_classification(classifications_df, genomic_accession):
    """Calculate the F1-score, recall (sensitivity), precision and specificity for
    CAZyme/non-CAZyme prediction.

    :param classifications_df: pandas df of CAZyme/non-CAZyme classifications
    :param genomic_accession: str, accession of the genomic assembly from which the test set is from

    Return F1-score, recall (sensitivity), precision and specificity, and summary dict.
    """
    y_true = classifications_df['CAZy'].to_numpy()  # convert to numpy array

    summary_lists = []  # [[stat, genome, tool, value]]

    # build a dict to store statistical parameters
    for tool in ["dbCAN", "HMMER", "Hotpep", "DIAMOND", "CUPP", "eCAMI"]:
        y_pred = classifications_df[tool].to_numpy()

        # calculations
        cm = confusion_matrix(y_true, y_pred)
        tn = cm[0][0]
        fn = cm[1][0]
        tp = cm[1][1]
        fp = cm[0][1]
        specificity_result = tn / (tn + fp)
        summary_lists.append(["Specificity", genomic_accession, tool, specificity_result])

        recall_result = recall_score(y_true, y_pred)
        summary_lists.append(["Recall", genomic_accession, tool, recall_result])

        precision_result = precision_score(y_true, y_pred)
        summary_lists.append(["Precision", genomic_accession, tool, precision_result])

        f1_result = f1_score(y_true, y_pred)
        summary_lists.append(["F1-score", genomic_accession, tool, f1_result])

        accuracy = (tp + tn)/(tp + fp + fn + tn)
        summary_lists.append(["Accuracy", genomic_accession, tool, accuracy])

    return summary_lists


def bootstrap_binary_classifications(all_binary_dfs, time_stamp, args):
    """Bootstrap resample binary CAZyme/non-CAZyme classifications to evaluated the expected
    range in performance of each prediciton tool.

    :param all_binary_dfs: list of ClassificationDFs, each one is a pandas df with asscoiated meta
    data
    :param time_stamp: str, time when evaluation started
    :param args: cmd-line args parser

    Return nothing.
    """
    # Perform bootstrapping of CAZyme/non-CAZyme predictions
    bootstrap_results = []
    #  bootstrap_results = [[genomic_accession, prediction_tool, bootstrap_number, accuracy_score]]

    binary_dfs = random.sample(all_binary_dfs, args.bs_sample_size)

    for tool in ["dbCAN", "HMMER", "Hotpep", "DIAMOND", "CUPP", "eCAMI"]:
        for df in tqdm(binary_dfs, desc=f"Bootstrapping accuracies for {tool}"):
            temp_df = pd.concat([df.df[tool], df.df["CAZy"]], axis=1, keys=None)

            # bootstrap the accuracy
            bs_acc = bootstrap_acc(temp_df, args.bs_resampling)
            bs_number = 1
            for result in bs_acc:
                bootstrap_results.append([df.genome_id, tool, bs_number, result])
                bs_number += 1

    bootstrap_results = pd.DataFrame(
        bootstrap_results,
        columns=['Genomic_accession', 'Prediction_tool', 'Bootstrap_number', 'accuracy'],
    )
    bootstrap_results.to_csv(f'bootstrap_accuracy_evaluation_{time_stamp}.csv')
    # USED FOR EVALUATION IN R

    return


def calc_acc(y_true, y_pred):
    """Calculate accuracy.

    :param y_true: ground truths, pandas series
    :param y_pred: predictions, pandas series

    Return float.
    """
    cm = confusion_matrix(y_true, y_pred)
    tn = cm[0][0]
    fn = cm[1][0]
    tp = cm[1][1]
    fp = cm[0][1]
    accuracy = (tp + tn)/(tp + fp + fn + tn)

    return accuracy


def bootstrap_acc(df, n):
    """Bootstrap accuracy.

    :param df: Pandas dataframe. 2 columns. First is predicted, second is ground truth
    :param n: int, number of times to resample

    Return tuple (bs.lower, bs.median, bs.upper).
    """
    bootstraps = []
    df_array = df.to_numpy()
    for _ in range(n):
        # create sample with replacement
        sample = resample(df_array)
        bootstraps.append(calc_acc(sample[:, 1], sample[:, 0]))

    return bootstraps