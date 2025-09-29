#! /usr/bin/env python

#! /usr/bin/env python
"""
score_text.py

This is an example script for how to score a text file using a vLLM server.

Usage:
    python scripts/score_text.py \
        -t data/rcv1-uc-irvine-subset/reuter5050/C50train/AaronPressman/401260newsML.txt \
        -m /disk1/dma0523/models/llama3.1-8b-w4a16 -p 8765
    python scripts/score_text.py \
        -t data/rcv1-uc-irvine-subset/reuter5050/C50train/AaronPressman/407599newsML.txt  \
        -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9000
"""
import argparse

import requests


def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score a text file using a vLLM server")
    parser.add_argument(
        "--textfile",
        "-t",
        type=str,
        required=True,
        help="/path/to/textfile",
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


def load_text_from_file(path: str) -> str:
    with open(path) as f:
        lines = f.readlines()
    return "".join(lines)


def extract_prompt_logprobs(
    server: str,
    model: str,
    text: str,
) -> list[tuple[str, int, float] | None]:
    """Get the per-token prompt tokens and logprobs for the given text.

    Args:
        server (str): Server URL
        model (str): Model name
        text (str): Input text

    Returns:
        list[Optional[tuple[str, int, int, float]]]: List of tuples containing
            - None for tokens without logprobs (e.g., special tokens)
            - (str(token), token_id, rank, logprob) for tokens with logprobs
    """
    #   Request completions with logprobs
    #   max_tokens = 0 is not supported
    r = requests.post(
        f"{server}/v1/completions",
        json={
            "model": model,
            "prompt": text,
            "max_tokens": 1,
            "prompt_logprobs": 1,
            "logprobs": 0,
            "echo": True,
            "temperature": 0.0,
        },
    )
    data = r.json()
    if "error" in data:
        print(f"Error from server: {data['error']}")
        return

    choices = data.get("choices")
    choice = choices[0]
    print(f"choice = {choice.keys()}")

    print(f"Response text : {choice["text"][:100]}...")

    # list[None|dict[str, {logprob, ...}]]
    plps = []
    prompt_logprobs = choice.get("prompt_logprobs")
    if prompt_logprobs is None:
        raise ValueError(f"Missing prompt fields; keys={list(choice.keys())}")

    for prompt_logprob in prompt_logprobs:
        if prompt_logprob is None:
            plps.append(None)
            continue

        #   Iterate through dict of token_id -> {logprob, rank, decoded_token}
        #   We want to take highest ranking token (largest number),
        #       which signifies the input token we provided
        best_token_id = max(
            prompt_logprob.items(),
            key=lambda x: x[1]["rank"],
        )[0]
        best_token_info = prompt_logprob[best_token_id]
        plps.append(
            (
                best_token_info["decoded_token"],
                int(best_token_id),
                int(best_token_info["rank"]),
                float(best_token_info["logprob"]),
            )
        )
    return plps


def main(args: argparse.Namespace) -> None:
    server = f"http://{args.host}:{args.port}"
    text = load_text_from_file(args.textfile)
    print(f"Loaded text : {text[:100]}...{text[-100:]}")
    logprobs: list[tuple[str, int, float] | None] = extract_prompt_logprobs(
        server=server,
        model=args.model,
        text=text,
    )

    print("Token String, Token ID, Rank, LogProb")
    # print("\t".join(prompt_token_ids[:20]))
    print(f"LPs : {logprobs[:20]}")
    print("...")
    print(f"...{logprobs[-20:]}")
    # print(f"tokens={len(vals)} mean_lp={mean_lp:.4f} ppl={ppl:.2f}")
    returned_text = "".join([t[0] if t is not None else "" for t in logprobs])
    if returned_text == text:
        print("Returned text matches input text!!")
    else:
        print("Returned text does NOT match input text!!")
        # d = difflib.Differ()
        # diff = d.compare(text.split(), returned_text.split())

        # # Print the differences
        # for line in diff:
        #     print(line)


if __name__ == "__main__":
    args = get_cli_args()
    main(args)
