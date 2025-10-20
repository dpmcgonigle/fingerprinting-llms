#! /usr/bin/env python

#! /usr/bin/env python
"""
score_text.py

This is an example script for how to score a text file using a vLLM server.

Usage:
    python scripts/score_text.py \
        -i data/rcv1-uc-irvine-subset/reuter5050/C50train/AaronPressman/407599newsML.txt  \
        -o data/tokens/llama3.1-70b-w4a16/reuter5050/C50train/AaronPressman/407599newsML.txt.npz  \
        -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9003
    
    for FILE in $(cat PRESSMAN.txt); do 
        python scripts/score_text.py \
            -i data/rcv1-uc-irvine-subset/reuter5050/C50train_clean/AaronPressman/$FILE \
            -o data/tokens/human/reuter5050/C50train/AaronPressman/${FILE}.npz \
            -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9003
    done
        
    for FILE in $(cat PRESSMAN.txt); do 
        python scripts/score_text.py \
            -i data/llama70Bw4a16/reuter5050/C50train_clean/AaronPressman/$FILE \
            -o data/tokens/llama70Bw4a16-bigmixtral-graded/reuter5050/C50train/AaronPressman/${FILE}.npz \
            -m /proj/redline/team/mcg/models/Mixtral-8x7B-Instruct-v0.1 -p 9999
    done
"""
import os
import logging
import argparse

from fingerprinting_llms.io.logger import setup_logger
from fingerprinting_llms.score import LogProbs
from fingerprinting_llms.score.extract import (
    load_text_from_file,
    extract_prompt_logprobs,
)


logger = logging.getLogger(__name__)


def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score a text file using a vLLM server")
    parser.add_argument(
        "--input-filepath",
        "-i",
        type=str,
        required=True,
        help="/path/to/input-filepath",
    )
    parser.add_argument(
        "--output-filepath",
        "-o",
        type=str,
        required=True,
        help="/path/to/input-filepath",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        required=True,
        help="/path/to/model",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host of the vLLM server",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8000,
        help="Port of the vLLM server",
    )
    return parser.parse_args()


def score_doc(
    server: str,
    model: str,
    input_filepath: str,
    output_filepath: str,
) -> None:
    text = load_text_from_file(filepath=input_filepath)
    logger.info(f"Loaded text : {text[:100]}...{text[-100:]}")
    #   (str(token), token_id, rank, logprob)
    logprobs: LogProbs = extract_prompt_logprobs(
        server=server,
        model=model,
        text=text,
    )

    # logger.info("\t".join(prompt_token_ids[:20]))
    logger.info(f"Tokens : {logprobs.decoded_tokens[:6]}...{logprobs.decoded_tokens[-6:]}")
    logger.info(f"Ranks : {logprobs.token_ranks[:6]}...{logprobs.token_ranks[-6:]}")
    logger.info(f"LPs : {logprobs.token_probs[:6]}...{logprobs.token_probs[-6:]}")
    # logger.info(f"tokens={len(vals)} mean_lp={mean_lp:.4f} ppl={ppl:.2f}")
    returned_text = "".join(logprobs.decoded_tokens.tolist())
    if returned_text == text:
        logger.info("Returned text matches input text!!")
    else:
        logger.info("Returned text does NOT match input text!!")

    logprobs.save_npz(filepath=output_filepath)

def main(args: argparse.Namespace) -> None:
    server = f"http://{args.host}:{args.port}"
    score_doc(server=server, model=args.model, input_filepath=args.input_filepath, output_filepath=args.output_filepath)


if __name__ == "__main__":
    args = get_cli_args()
    log_file = f"{os.path.splitext(__file__)[0]}.log"
    setup_logger(log_file=log_file, log_level=logging.INFO)
    main(args)
