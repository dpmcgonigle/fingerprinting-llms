#   Fingerprinting LLMs Meetings

##  Contents
- [Project Description](#2025-09-19)
- [Project Documentation](#2025-09-05)

## 2025-09-19
Having looked into several datasets, I took a subset of a larger Reuters dataset (RCV1), which was compiled by UC Irvine.  See data/rcv1-uc-irvine-subset/reuter5050/README.md for more details.  I created a notebook with some Exploratory Data Analysis into this dataset in the home directory of this repository.

During the meeting, we discussed some of the technical challenges and next steps:
- Get LLM running
- See if we can get log probabilities for all human-generated text
- Find Essay dataset
- Perform EDA on Essay dataset
- Dataset Cleaning
- Generate LLM corpus
- Compare distributions between LLM and human

### Get LLM Running
See serving/download_model.py and serve-metal.sh for scripts that can download and then serve models locally.  I decided to serve the LLMs on "metal" (as opposed to docker) for speed and practical purposes.  I was able to get the following versions of Llama 3.1 running:
- https://huggingface.co/RedHatAI/Meta-Llama-3.1-8B-Instruct-quantized.w4a16
- https://huggingface.co/RedHatAI/Meta-Llama-3.1-70B-Instruct-quantized.w4a16
Note: The "w4a16" signifies Weight-only 4-bit, Activation-only 16-bit quantization, which means it requires much less GPU memory.  The 8B quantized model can be run on a 24GB GPU (RTX 3090, for instance), while the 70B quantized model cna be run on a 48GB GPU (A6000, for instance).  Note that running the full 70B version would require 4x A6000 (~200GB GPU memory), while the full 8B version would require 1x A6000 (32GB GPU memory).

### Get LogProbs for Human-Generated Text
One of the main concerns that Professor Roos raised is whether we can actually get all of the log probabilities for all tokens within a human-generated text.  I was able to accomplish this; see SCORING_TEXT.md for details.

### Find Essay Dataset
TODO

### Perform EDA on Essay Dataset
TODO

### Dataset Cleaning
As mentioned in the previous meeting notes, I don't want the difference in signal between the human-generated and llm-generated text to be spelling errors and grammatical faux pas.  I similarly don't want there to be some sort of structural item that differs between the two bodies (think Enigma code broken by the allies in WWII).  Some thought will need to go into how best to accomplish this.

### Generate LLM Corpus
TODO 

### Compare Distributions Between LLM and Human Corpora
TODO

[Back To Top](#fingerprinting-llms-meetings)

## 2025-09-05
This was our first meeting for the project.  We discussed the meeting schedule, the project requirements, project details, and first steps.

### Meeting Schedule
Every two weeks, aiming for Fridays at 0800 EDT (0600 MDT).  We will flex for days that don't work for both of us.

### Project Requirements
We're required to turn in Form 4750, which requires us to determine:
- Project Title: "Finterprinting Large Language Models with Signal Processing"
- Advisor Meeting Schedule: See above
- First Draft Date: Nov 12, 2025
- Presentation Date: Dec 11 at 0900 EST

### First Steps
An important prerequisite for this project is performing due diligence with respect to our dataset. I came into the meeting with some inital thoughts on what would make for a good dataset:
- Semi-professional; I don't want our signal differences to be due to spelling errors and poor grammar.
- A corpous of documents that are moderate (aim for ~500+ words) in length; provide the LLM with enough runway to impart patterns.
- A corpus that was created/collected before the advent of LLMs; I don't want to be questioning whether the "human-generated" documents were in-fact LLM-generated.

We narrowed our search for datasets down to student essays, news articles, and similar bodies of text that might fit these constraints.

[Back To Top](#fingerprinting-llms-meetings)
