#! /usr/bin/env python
"""
score_text.py

This is an example script for how to score a text file using a vLLM server.

Usage:
    python scripts/score_text.py \
        -i data/rcv1-uc-irvine-subset/reuter5050/C50train/AaronPressman/407599newsML.txt  \
        -o data/tokens/llama3.1-70b-w4a16/reuter5050/C50train/AaronPressman/407599newsML.txt.npz  \
        -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9003
    
    for FILE in $(find data/rcv1-uc-irvine-subset/reuter5050/C50train_clean/ -type f); do echo $FILE >> HUMAN.txt; done
    for FILE in $(cat HUMAN.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/rcv1-uc-irvine-subset/tokens\/human_llama-graded}.npz \
            -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9003
    done

    for FILE in $(cat HUMAN.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/rcv1-uc-irvine-subset/tokens\/human_bigmixtral-graded}.npz \
            -m /proj/redline/team/mcg/models/Mixtral-8x7B-Instruct-v0.1 -p 9002
    done
        
    for FILE in $(find data/llama70Bw4a16/reuter5050/C50train_clean/ -type f); do echo $FILE >> LLAMA.txt; done
    for FILE in $(cat LLAMA.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/llama70Bw4a16/tokens\/llama70Bw4a16}.npz \
            -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9003
    done

    for FILE in $(find data/mixtral-8x7B-instruct/reuter5050/C50train_clean/ -type f); do echo $FILE >> MIXTRAL.txt; done
    for FILE in $(cat MIXTRAL.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/mixtral-8x7B-instruct/tokens\/llama70Bw4a16-bigmixtral-graded}.npz \
            -m /proj/redline/team/mcg/models/Mixtral-8x7B-Instruct-v0.1 -p 9002
    done
    for FILE in $(cat MIXTRAL.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/mixtral-8x7B-instruct/tokens\/bigmixtral-llama70Bw4a16-graded}.npz \
            -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9000
    done

    HC3
    for FILE in $(find data/hc3/human_answers/ -type f); do echo $FILE >> HC3_HUMAN.txt; done
    for FILE in $(find data/hc3/chatgpt_answers/ -type f); do echo $FILE >> HC3_CHATGPT.txt; done

    for FILE in $(cat HC3_HUMAN.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/hc3/tokens\/human_llama-graded}.npz \
            -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9001
    done
    for FILE in $(cat HC3_CHATGPT.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/hc3/tokens\/chatgpt_llama-graded}.npz \
            -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9001
    done

    for FILE in $(cat HC3_HUMAN.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/hc3/tokens\/human_mixtral-graded}.npz \
            -m /proj/redline/team/mcg/models/Mixtral-8x7B-Instruct-v0.1 -p 9002
    done
    for FILE in $(cat HC3_CHATGPT.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/hc3/tokens\/chatgpt_mixtral-graded}.npz \
            -m /proj/redline/team/mcg/models/Mixtral-8x7B-Instruct-v0.1 -p 9002
    done

    MAGE
    for FILE in $(find data/mage/human/ -type f); do echo $FILE >> MAGE_HUMAN.txt; done
    for FILE in $(find data/mage/llm/ -type f); do echo $FILE >> MAGE_LLM.txt; done

    for FILE in $(cat MAGE_HUMAN.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/mage/tokens\/mage\/human_llama-graded}.npz \
            -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9001
    done
    for FILE in $(cat MAGE_LLM.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/mage/tokens\/mage\/llm_llama-graded}.npz \
            -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9001
    done

    for FILE in $(cat MAGE_HUMAN.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/mage/tokens\/mage\/human_mixtral-graded}.npz \
            -m /proj/redline/team/mcg/models/Mixtral-8x7B-Instruct-v0.1 -p 9002
    done
    for FILE in $(cat MAGE_LLM.txt); do 
        printf "\n\n*   *   *   *   STARTING $FILE  *   *   *"
        python scripts/score_text.py \
            -i $FILE \
            -o ${FILE/mage/tokens\/mage\/llm_mixtral-graded}.npz \
            -m /proj/redline/team/mcg/models/Mixtral-8x7B-Instruct-v0.1 -p 9002
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
