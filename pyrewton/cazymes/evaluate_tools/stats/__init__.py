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
"""Module for statistical evaluation of CAZyme prediction tools

:class ClassificationDF: Represents a CAZyme/non-CAZyme annotation/classification df for a test set

:func evaluate_performance: Co-ordinates overall evaluation of prediction tools
:func parse_predictions: Parses the raw output files from the CAZyme prediction tools

"""


import pandas as pd

from datetime import datetime

from tqdm import tqdm

from pyrewton.cazymes.evaluate_tools.parse import (
    parse_dbcan_output,
    parse_cupp_output,
    parse_ecami_output,
)
from pyrewton.cazymes.evaluate_tools.stats import (
    binary_cazyme_noncazyme_classification as binary_classification
)
from pyrewton.cazymes.evaluate_tools.stats import (
    multilabel_family_classification as multilabel_classification
)


class ClassificationDF:
    """Represents a CAZyme/non-CAZyme annotation/classification df for a test set"""

    def __init__(self, genome_id, df):
        self.genome_id = genome_id
        self.df = df

    def __str__(self):
        return f"<CAZyme/non-CAZyme classification df for test set {self.genome_id}>"

    def __repr__(self):
        return f"<CAZyme/non-CAZyme classification df for test set {self.genome_id}>"


def evaluate_performance(predictions, cazy_dict, args):
    """Evaluate the performance of the CAZymes prediction tools.

    Binary classification: CAZyme/non-CAZyme differentiation
    Multilabel classification (MLC): CAZy family predictions

    :param predictions: list of TestSet class instances
    :param cazy_dict: dict keyed by GenBank protein accession, valued by CAZy family classifications
    :param args: cmd-line args parser

    Return nothing.
    """
    time_stamp = datetime.now().strftime("%Y_%m_%d")

    fam_dict = multilabel_classification.foundation_dict()
    # fam_dict used to form foundation of multilabel classification

    (
        all_binary_c_nc_dfs,
        binary_c_nc_statistics,
        mlc_predictions,
        mlc_ground_truths,
    ) = parse_predictions(
        predictions, time_stamp, cazy_dict,
    )

    binary_stat_df = pd.DataFrame(
        binary_c_nc_statistics,
        columns=['Statistic parameter', 'Genomic assembly', 'Prediction tool', 'Statistic value'],
    )
    binary_stat_df.to_csv(f'binary_classification_evaluation_{time_stamp}.csv')  # USED FOR EVALUATION IN R

    binary_classification.bootstrap_binary_c_nc_classifications(all_binary_c_nc_dfs, args)

    column_names = ["Genomic_accession", "Protein_accession", "Prediction_tool"]
    column_names += list(fam_dict.keys())
    mlc_predictions = pd.DataFrame(mlc_predictions, columns=column_names)
    mlc_predictions.to_csv(f"mlc_evaluation_{time_stamp}.csv")   # USED FOR EVALUATION IN R

    mlc_ground_truths = pd.DataFrame(mlc_ground_truths, columns=column_names)
    mlc_ground_truths.to_csv(f"mlc_ground_truths_{time_stamp}.csv")   # USED FOR EVALUATION IN R

    # evaluate the performance of predicting the correct CAZy family
    multilabel_classification.calc_fam_fbeta_score(
        mlc_predictions,
        mlc_ground_truths,
        time_stamp,
        args,
    )  # USED FOR EVALUATION IN R
    multilabel_classification.calc_fam_fbeta_score_per_testset(
        mlc_predictions,
        mlc_ground_truths,
        time_stamp,
        predictions,
        args,
    )  # USED FOR EVALUATION IN R
    multilabel_classification.calc_fam_stats(
        mlc_predictions,
        mlc_ground_truths,
        time_stamp,
        args,
    )  # USED FOR EVALUATION IN R

    # evaluate the performance of predicting the correct CAZy class
    multilabel_classification.build_class_dataframes(
        mlc_predictions,
        mlc_ground_truths,
        args,
        time_stamp,
    )  # USED FOR EVALUATION IN R

    return


def parse_predictions(predictions, time_stamp, cazy_dict):
    """Parse prediction outputs from prediction tools and create dataframes for the stats eval.

    :param predictions: list of TestSet class instances
    :param time_stamp: str, data and time when evaluation started, used for naming files
    :param cazy_dict: dict keyed by GenBank protein accession, valued by CAZy family classifications

    Return:
    all_binary_c_nc_dfs - list of pandas dfs of binary CAZyme/non-CAZyme predicitons, one df is
        created per test set containing CAZmye/non-CAZyme predictions from all prediction tools,
        and the ground truths from CAZy. This is used for bootstrapping the accuracy.
    binary_c_nc_statistics - list of lists of statistical parameter values for each test set, for
        each prediction tool, evaluating CAZymes and non-CAZyme predictions (written in long form)
    mlc_predictions - list of CAZy family predictions, written in tidy/long form
    mlc_ground_truths - list of known CAZy family, written in tidy/long form
    """
    all_binary_c_nc_dfs = []  # used for bootstrapping accuracy
    binary_c_nc_statistics = []  # [[stat, genomic assembly, prediction tool, value]]

    mlc_predictions = []  # [[assembly, protein, prediction tool, fam1, fam2, fam3...]]
    mlc_ground_truths = []  # [[assembly, protein, prediction tool, fam1, fam2, fam3...]]

    for test_set in tqdm(predictions, desc="Standardising outputs"):
        # create paths to the raw prediction tool output files to be parsed
        dir_path = test_set.prediction_paths["dir"]
        test_set.prediction_paths["dbcan"] = dir_path / "overview.txt"
        test_set.prediction_paths["hotpep"] = dir_path / "Hotpep.out"
        test_set.prediction_paths["cupp"] = dir_path / "cupp_output.fasta.log"
        test_set.prediction_paths["ecami"] = dir_path / "ecami_output.txt"

        # standardise the raw outputs from the prediction tools
        # tool_predictions is a list of CazymeProteinPrediction instances
        # (see evaluate_tools.parse.__init__.py)
        (
            hmmer_predictions,
            hotpep_predictions,
            diamond_predictions,
            dbcan_predictions,
        ) = parse_dbcan_output.parse_dbcan_output(
            test_set.prediction_paths["dbcan"],
            test_set.prediction_paths["hotpep"],
            test_set.fasta,
        )

        cupp_predictions = parse_cupp_output.parse_cupp_output(
            test_set.prediction_paths["cupp"],
            test_set.fasta,
        )

        ecami_predictions = parse_ecami_output.parse_ecami_output(
            test_set.prediction_paths["ecami"],
            test_set.fasta,
        )

        standardised_outputs = {
            "dbCAN": dbcan_predictions,
            "HMMER": hmmer_predictions,
            "Hotpep": hotpep_predictions,
            "DIAMOND": diamond_predictions,
            "CUPP": cupp_predictions,
            "eCAMI": ecami_predictions,
        }

        binary_classifications = []  # store all binary C/NC classifications for this test set

        for tool in tqdm(standardised_outputs, "Adding raw predictions to cumlative dfs"):

            # parse binary CAZyme/non-CAZyme predictions for the prediction tool
            all_binary_classifications = binary_classification.get_predicted_classifications(
                standardised_outputs[tool],
                tool,
                all_binary_classifications,
            )

            # parse multilabel classficiation (mlc) of CAZy family predictions
            (
                mlc_prediction, mlc_ground_truth,
            ) = multilabel_classification.get_multilable_classifications(
                tool[0],
                tool[1],
                cazy_dict,
                test_set.source,
            )

            # parse multilabel classficiation (mlc) of CAZy class predictions ???
            ???

            mlc_predictions += mlc_prediction
            mlc_ground_truths += mlc_ground_truth

        # build a datafame of containing all binary C/NC classifications from all prediction
        # tools for this test set
        classifications_df = binary_classification.build_classification_df(
            all_binary_classifications,
        )

        # add ground truth (CAZy) binary CAZyme/non-CAZyme classifications to classifications.df
        classifications_df = binary_classification.add_ground_truths(
            classifications_df, cazy_dict,
        )

        classifications_df.to_csv(f"binary_classifications_{time_stamp}_{test_set.source}.csv")

        all_binary_c_nc_dfs.append(ClassificationDF(test_set.source, classifications_df))
        # all_binary_c_nc_dfs used for bootstrapping accuracy of binary predictions

        # calculate statistics parameters for each tool performance, evaluating the binary
        # classification of CAZymes and non-CAZymes
        binary_c_nc_statistics += binary_classification.evaluate_binary_classifications(
            classifications_df, test_set.source, args,
        )

    return all_binary_c_nc_dfs, binary_c_nc_statistics, mlc_predictions, mlc_ground_truths
