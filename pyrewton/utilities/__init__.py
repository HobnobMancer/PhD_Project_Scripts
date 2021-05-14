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
"""Module for building loggers and cmd-line args parsers for pyrewton modules."""

import logging


def config_logger(args) -> logging.Logger:
    """Configure package wide logger.
    Configure a logger at the package level, from which the module will inherit.
    If CMD-line args are provided, these are used to define output streams, and
    logging level.
    :param args: cmd-line args parser
    Return nothing
    """
    logger = logging.getLogger(__package__)

    # Set format of loglines
    log_formatter = logging.Formatter("[%(levelname)s] [%(name)s]: %(message)s")

    # define logging level
    if args.verbose is True:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    # Setup console handler to log to terminal
    console_log_handler = logging.StreamHandler()
    console_log_handler.setFormatter(log_formatter)
    logger.addHandler(console_log_handler)

    # Setup file handler to log to a file
    if args.log is not None:
        file_log_handler = logging.FileHandler(args.log)
        file_log_handler.setFormatter(log_formatter)
        logger.addHandler(file_log_handler)

    return


def build_logger(output, file_name):
    """Build loggers with pre-defined parameters for writing out errors and failed scrapes.

    :param output: Path to output dir or None
    :param file_name: str, name of output log file

    Return logger object.
    """
    logger = logging.getLogger(file_name[:-4])

    if output is None:
        output = os.getcwd()
        path_ = Path(f"{output}/{file_name}")
    else:
        path_ = output / f"{file_name}"

    # Set format of loglines
    log_formatter = logging.Formatter(file_name + ": {} - {}".format("%(asctime)s", "%(message)s"))

    # Setup file handler to log to a file
    file_log_handler = logging.FileHandler(path_)
    file_log_handler.setLevel(logging.WARNING)
    file_log_handler.setFormatter(log_formatter)
    logger.addHandler(file_log_handler)

    return logger
