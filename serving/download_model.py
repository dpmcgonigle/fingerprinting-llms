#! /usr/bin/env python
"""
download_model.py

Download a model from Hugging Face Hub

Usage:
    python download_model.py \
        --hf-token YOUR_HF_TOKEN \
        --repo-id "neuralmagic/Meta-Llama-3.1-8B-Instruct-quantized.w4a16" \
        --model-dir /disk1/dma0523/models/llama3.1-8b-w4a16

    python download_model.py \
        --hf-token YOUR_HF_TOKEN \
        --repo-id "neuralmagic/Meta-Llama-3.1-70B-Instruct-quantized.w4a16" \
        --model-dir /disk1/dma0523/models/llama3.1-70b-w4a16
"""
import os
import argparse

from huggingface_hub import snapshot_download

def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a model from Hugging Face Hub"
    )
    parser.add_argument(
        "--hf-token",
        type=str,
        required=True,
        help="Hugging Face token with access to the model",
    )
    parser.add_argument(
        "--repo-id",
        type=str,
        required=True,
        help="Hugging Face repository ID of the model to download",
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        required=True,
        help="Local directory to save the downloaded model",
    )
    return parser.parse_args()

def main(args: argparse.Namespace) -> None:
    os.makedirs(args.model_dir, exist_ok=True)
    snapshot_download(
        token=args.hf_token,
        repo_id=args.repo_id,
        local_dir=args.model_dir,
        local_dir_use_symlinks=False,
    )

if __name__ == "__main__":
    args = get_cli_args()
    main(args)