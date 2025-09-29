#! /usr/bin/env python
"""
preprocess_text.py

Example:
    python scripts/preprocess_text.py \
        -i data/rcv1-uc-irvine-subset/reuter5050/C50train/AaronPressman/401260newsML.txt \
        -o data/rcv1-uc-irvine-subset/reuter5050defaultclean/C50train/AaronPressman/401260newsML.txt
"""

import argparse
import logging
import os

from fingerprinting_llms.io.logger import setup_logger
from fingerprinting_llms.preprocess.text import (
    TextPreprocessor,
    TextPreprocessorConfig,
)

logger = logging.getLogger(__name__)


def get_cli_args() -> argparse.Namespace:
    log_file = f"{os.path.splitext(__file__)[0]}.log"
    parser = argparse.ArgumentParser(description="Preprocess a text file")
    parser.add_argument(
        "--inputfile",
        "-i",
        type=str,
        required=True,
        help="/path/to/inputfile",
    )
    parser.add_argument(
        "--outputfile",
        "-o",
        type=str,
        required=True,
        help="/path/to/outputfile",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--logfile",
        "-l",
        default=log_file,
        type=str,
        help="Path to log file",
    )
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:

    config = TextPreprocessorConfig()
    preprocessor = TextPreprocessor.from_config(cfg=config)

    logger.info(f"Loading text from {args.inputfile}")
    with open(args.inputfile) as f:
        text = f.read()

    logger.info("Preprocessing text")
    cleaned_document = preprocessor.clean_document(text=text)

    logger.info(f"Saving processed text to {args.outputfile}")
    os.makedirs(os.path.dirname(args.outputfile), exist_ok=True)
    with open(args.outputfile, "w") as f:
        f.write(cleaned_document.clean_text)

    logger.info("Preprocessing complete")


if __name__ == "__main__":
    args = get_cli_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logger(log_file=args.logfile, log_level=log_level)
    main(args)
