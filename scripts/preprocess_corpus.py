#! /usr/bin/env python
"""
preprocess_text.py

Example:
    python scripts/preprocess_text.py \
        -i data/rcv1-uc-irvine-subset/reuter5050/C50train \
        -o data/rcv1-uc-irvine-subset/reuter5050/C50train_clean
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
        "--inputdir",
        "-i",
        type=str,
        required=True,
        help="/path/to/inputdir",
    )
    parser.add_argument(
        "--outputdir",
        "-o",
        type=str,
        required=True,
        help="/path/to/outputdir",
    )
    parser.add_argument(
        "--extensions",
        "-e",
        type=str,
        nargs="*",
        default=(".txt"),
        help="/path/to/outputdir",
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
    args = parser.parse_args()

    #   Validate
    if args.inputdir == args.outputdir:
        raise ValueError(f"Can't overwrite same directory")

    return args


def main(args: argparse.Namespace) -> None:

    config = TextPreprocessorConfig()
    preprocessor = TextPreprocessor.from_config(cfg=config)

    logger.info(f"Searching for files in {args.inputdir}")

    # Use os.walk to get all .txt files in the directory
    txt_files = []
    for root, _, files in os.walk(args.inputdir):
        for file in files:
            if file.endswith(args.extensions):
                txt_files.append(os.path.join(root, file))

    logger.info(f"Found {len(txt_files)} {args.extensions} files")

    # Create output directory if it doesn't exist
    os.makedirs(args.outputdir, exist_ok=True)

    # Process each text file
    for txt_file in txt_files:
        # Get relative path to maintain directory structure in output
        rel_path = os.path.relpath(txt_file, args.inputdir)
        output_file = os.path.join(args.outputdir, rel_path)

        # Create output subdirectories if needed
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        logger.info(f"Processing {rel_path}")
        with open(txt_file, "r") as f:
            text = f.read()

        # Preprocess the text
        cleaned_document = preprocessor.clean_document(text=text)

        # Save the processed text
        cleaned_document.save(output_file)
        logger.info(f"Saved {output_file}")

    logger.info(f"All files processed and saved to {args.outputdir}")

    logger.info("Preprocessing complete")


if __name__ == "__main__":
    args = get_cli_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logger(log_file=args.logfile, log_level=log_level)
    main(args)
