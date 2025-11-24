# Human ChatGPT Comparison Corpus (HC3) Dataset
This is a dataset that compares how well ChatGPT (using GPT3.5 and GPT4) compares to human authors.  

## Data
You can download the data from https://huggingface.co/datasets/Hello-SimpleAI/HC3.

## HC3 Description
The HC3 (How Close is ChatGPT to Human Experts?) dataset is a corpus designed to compare human-written answers with ChatGPT-generated answers to the same questions. It contains thousands of question–answer pairs (~10K questions) collected from finance, medicine, Reddit ELI5, Wikipedia, and open-ended general knowledge domains. For each question, the dataset includes one or more human expert answers and one or more ChatGPT. Both the human and AI answers are typically multi-sentence and often multi-paragraph, enabling analysis of style, coherence, factuality, and linguistic differences at longer scales. 

## HC3 Preprocessing
The only pre-processing I've done is to select only those articles that are 200 words or greater, filtering out short answers.
