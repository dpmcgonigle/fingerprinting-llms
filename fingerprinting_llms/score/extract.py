import logging
import requests

from fingerprinting_llms.score import LogProbs

logger = logging.getLogger(__name__)



def load_text_from_file(filepath: str) -> str:
    with open(filepath) as f:
        lines = f.readlines()
    return "".join(lines)


def extract_prompt_logprobs(
    server: str,
    model: str,
    text: str,
) -> LogProbs:
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
        logger.warning(f"Error from server: {data['error']}")
        return

    choices = data.get("choices")
    choice = choices[0]
    logger.info(f"choice = {choice.keys()}")

    logger.info(f"Response text : {choice["text"][:100]}...")

    # list[None|dict[str, {logprob, ...}]]
    prompt_logprobs = choice.get("prompt_logprobs")
    if prompt_logprobs is None:
        raise ValueError(f"Missing prompt fields; keys={list(choice.keys())}")

    decoded_tokens: list[str] = []
    token_ids: list[int] = []
    token_ranks: list[int] = []
    token_probs: list[float] = []
    for prompt_logprob in prompt_logprobs:
        if prompt_logprob is None:
            continue

        #   Iterate through dict of token_id -> {logprob, rank, decoded_token}
        #   We want to take highest ranking token (largest number),
        #       which signifies the input token we provided
        best_token_id = max(
            prompt_logprob.items(),
            key=lambda x: x[1]["rank"],
        )[0]
        best_token_info = prompt_logprob[best_token_id]
        decoded_tokens.append(best_token_info["decoded_token"])
        token_ids.append(int(best_token_id))
        token_ranks.append(int(best_token_info["rank"]))
        token_probs.append(float(best_token_info["logprob"]))

    log_probs = LogProbs.from_lists(
        decoded_tokens=decoded_tokens,
        token_ids=token_ids,
        token_ranks=token_ranks,
        token_probs=token_probs,
    )
    logger.info(f"Created log_probs of size {log_probs.size}")
    return log_probs
