import os

from datasets import load_dataset


def meets_word_threshold(text: str, threshold=200) -> bool:
    """Check if any answer in the list meets the word threshold."""
    if len(text.split()) >= threshold:
        return True
    return False

MIN_WORDS = 200

#   Keep track of skipped / kept files based on threshold
skipped = 0 
kept = 0

dataset = load_dataset("yaful/MAGE")
texts = dataset["test"]["text"]
labels = dataset["test"]["label"]
if len(texts) != len(labels):
    raise ValueError(f"Texts : {len(texts)}, Labels : {len(labels)}")

print(f"Loaded {len(texts)} texts and {len(labels)} labels")

human_dir = f"data/mage/human"
llm_dir = f"data/mage/llm"

os.makedirs(human_dir, exist_ok=True)
os.makedirs(llm_dir, exist_ok=True)

for i in range(len(texts)):
    text = texts[i]
    label = labels[i]
    #print(f"TEXT LEN {len(text)} ({len(text.split())} words)")

    enough_words = meets_word_threshold(text=text, threshold=MIN_WORDS)
    
    # Skip if either side is too short
    if not enough_words:
        print(f"Skipping question {i}; len {len(text.split())}")
        skipped += 1
        continue
    else:
        kept += 1

    # One file per text
    if int(label) == 1:
        fname = os.path.join(llm_dir, f"text_{i}_llm.txt")
    elif int(label) == 0:
        fname = os.path.join(human_dir, f"text_{i}_llm.txt")
    else:
        #print(f"Raising exception for label {label}")
        raise ValueError(f"Unknown label {label}")
    
    with open(fname, "w", encoding="utf-8") as f:
        #print(f"Writing to {fname}")
        f.write(text)

print(f"Kept {kept} texts, skipped {skipped}")