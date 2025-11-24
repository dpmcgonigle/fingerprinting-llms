import os

from datasets import load_dataset


def meets_word_threshold(answer_list: list[str], threshold=200) -> bool:
    """Check if any answer in the list meets the word threshold."""
    for answer in answer_list:
        if len(answer.split()) >= threshold:
            return True
    return False

MIN_WORDS = 200
TOPICS = [
    "finance",
    "medicine",
    "open_qa",
    "wiki_csai",
    "reddit_eli5",
]

#   Keep track of skipped / kept files based on threshold
skipped = 0 
kept = 0

for topic in TOPICS:
    dataset = load_dataset("Hello-SimpleAI/HC3", topic)
    train_ds = dataset["train"]

    ds_skipped = 0
    ds_kept = 0

    question_dir = f"data/hc3/questions/{topic}"
    human_dir = f"data/hc3/human_answers/{topic}"
    chatgpt_dir = f"data/hc3/chatgpt_answers/{topic}"

    os.makedirs(human_dir, exist_ok=True)
    os.makedirs(chatgpt_dir, exist_ok=True)
    os.makedirs(question_dir, exist_ok=True)

    for i, row in enumerate(train_ds):
        qid = row.get("id", i)

        human_answers = row["human_answers"]
        chatgpt_answers = row["chatgpt_answers"]

        # Normalize to list
        if isinstance(human_answers, str):
            human_answers = [human_answers]
        if isinstance(chatgpt_answers, str):
            chatgpt_answers = [chatgpt_answers]

        enough_human_words = meets_word_threshold(human_answers, threshold=MIN_WORDS)
        enough_llm_words = meets_word_threshold(chatgpt_answers, threshold=MIN_WORDS)
        
        # Skip if either side is too short
        if not (enough_human_words and enough_llm_words):
            print(f"Skipping question {qid}; meets threshold? human {enough_human_words}, llm {enough_llm_words}")
            ds_skipped += 1
            continue
        else:
            ds_kept += 1

        # Create question file
        fname = os.path.join(question_dir, f"q{qid}_question.txt")
        question = row["question"]
        with open(fname, "w", encoding="utf-8") as f:
            f.write(question)

        # One file per answer
        for j, ans in enumerate(human_answers):
            fname = os.path.join(human_dir, f"q{qid}_human_{j}.txt")
            with open(fname, "w", encoding="utf-8") as f:
                f.write(ans)

        for j, ans in enumerate(chatgpt_answers):
            fname = os.path.join(chatgpt_dir, f"q{qid}_chatgpt_{j}.txt")
            with open(fname, "w", encoding="utf-8") as f:
                f.write(ans)
    
    print(f"DATASET {topic} Kept {ds_kept} questions, skipped {ds_skipped}")
    kept += ds_kept
    skipped += ds_skipped
    
print(f"Kept {kept} questions, skipped {skipped}")