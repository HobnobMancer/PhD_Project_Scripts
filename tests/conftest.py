#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:
# Emma E. M. Hobbs

# Contact
# eemh1@st-andrews.ac.uk

# Emma E. M. Hobbs,
# Biomolecular Sciences Building,
# University of St Andrews,
# North Haugh Campus,
# St Andrews,
# KY16 9ST
# Scotland,
# UK

# The MIT License
"""Configuration file for pytest files.

Contains fixtures used by multiple test files.
"""

import json
import logging

from argparse import Namespace
from pathlib import Path

import pandas as pd

import pytest


@pytest.fixture
def dumpy_email():
    email = "dumpy.email@my.domain"
    return email


@pytest.fixture
def null_logger():
    logger = logging.getLogger("Test_ac_number_retrieval logger")
    logger.addHandler(logging.NullHandler())
    return logger


@pytest.fixture
def logger_output():
    output = Path("tests/")
    logger_output = (
        output / "test_targets" / "bld_lggr_test_targets" / "test_bld_logger.log"
    )
    return logger_output


@pytest.fixture
def logger_args(logger_output):
    argsdict = {"args": Namespace(verbose=False, log=logger_output)}
    return argsdict


@pytest.fixture
def testing_df():
    df_data = [["A", "B", "C"]]
    df = pd.DataFrame(df_data, columns=["C1", "C2", "C3"])
    return df


@pytest.fixture
def testing_df_output_file():
    output = Path("tests/")
    df_output = output / "test_targets" / "file_io_test_targets" / "test_writing_df.csv"
    return df_output


@pytest.fixture
def testing_df_output_dir():
    output = Path("tests/")
    df_output = output / "test_targets" / "file_io_test_targets"
    return df_output


@pytest.fixture
def file_io_args(testing_df_output_dir):
    argsdict = {
        "args": Namespace(output=testing_df_output_dir, nodelete=False, force=True)
    }
    return argsdict


@pytest.fixture
def gt_ncbi_gnms_input_dir():
    test_dir = Path("tests")
    input_dir = test_dir / "test_inputs" / "gt_ncbi_gnms_test_inputs"
    return input_dir


@pytest.fixture
def gt_ncbi_gnms_test_inputs(gt_ncbi_gnms_input_dir):
    with (gt_ncbi_gnms_input_dir / "gt_ncbi_gnms_test_inputs.json").open("r") as ifh:
        test_inputs = json.load(ifh)
        inputs = []
        inputs.append(test_inputs["retries"])
        inputs.append(test_inputs["taxonomy_id"])
        inputs.append(test_inputs["genus_species_name"])
        inputs.append(test_inputs["line_number"])
        inputs.append(test_inputs["df_row_genus"])
        inputs.append(test_inputs["df_row_species"])
    return inputs


# Define fixtures local to these tests
@pytest.fixture
def test_ncbi_species_file(gt_ncbi_gnms_input_dir):
    input_reading_path = gt_ncbi_gnms_input_dir / "gt_ncbi_gnms_reading_test_input.txt"
    return input_reading_path


@pytest.fixture
def input_ncbi_df(gt_ncbi_gnms_test_inputs):
    row_data = []
    row_data.append(gt_ncbi_gnms_test_inputs[4])
    row_data.append(gt_ncbi_gnms_test_inputs[5])
    row_data.append(gt_ncbi_gnms_test_inputs[1])
    return row_data


@pytest.fixture
def ncbi_args():
    argsdict = {"args": Namespace(genbank=False, retries=10, timeout=10)}
    return argsdict


@pytest.fixture
def gt_ncbi_gnms_targets():
    test_dir = Path("tests")
    target_dir = test_dir / "test_targets" / "gt_ncbi_gnms_test_targets"
    with (target_dir / "gt_ncbi_gnms_test_targets.json").open("r") as ifht:
        test_targets = json.load(ifht)
        target_sci_name = test_targets["target_genus_species_name"]
        target_tax_id = test_targets["target_taxonomy_id"]
    return target_sci_name, target_tax_id, target_dir


@pytest.fixture
def genbank_df_path():
    test_dir = Path("tests")
    genbank_df = (
        test_dir / "test_inputs" / "gt_gnbnk_anntns_test_inputs" / "test_input_df.csv"
    )
    return genbank_df


@pytest.fixture
def genbank_files_dir():
    test_dir = Path("tests")
    genbank_dir = (
        test_dir / "test_inputs" / "gt_gnbnk_anntns_test_inputs" / "test_genbank_files"
    )
    return genbank_dir


@pytest.fixture
def gnbnk_anno_args(genbank_files_dir):
    argsdict = {"args": Namespace(genbank=genbank_files_dir)}
    return argsdict


@pytest.fixture
def genbank_df(genbank_df_path):
    input_df = pd.read_csv(genbank_df_path, header=0, index_col=0)
    return input_df


@pytest.fixture
def formated_uniprot_results():
    test_dir = Path("tests")
    df_dir = (
        test_dir
        / "test_inputs"
        / "gt_unprt_prtns_test_inputs"
        / "mocked_formated_uniprot_results.csv"
    )
    df = pd.read_csv(df_dir, header=0, index_col=0)
    return df


@pytest.fixture
def unformated_uniprot_results():
    test_dir = Path("tests")
    df_dir = (
        test_dir
        / "test_inputs"
        / "gt_unprt_prtns_test_inputs"
        / "mocked_unformated_uniprot_results.csv"
    )
    df = pd.read_csv(df_dir, header=0, index_col=0)
    return df


@pytest.fixture
def uniprot_query_source(formated_uniprot_results):
    """Return single row, a pandas series."""
    return formated_uniprot_results.head(1)
