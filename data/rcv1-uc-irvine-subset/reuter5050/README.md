# Reuters 50/50 dataset
This is a subset of the RCV1 dataset, which is a collection of Reuters news articles from RCV1.

## Data
You can download the data from https://archive.ics.uci.edu/dataset/217/reuter+50+50, and put the corresponding "C50test" and "C50train" files in this directory to run the EDA notebook.

## RCV1 Description
The RCV1 (Reuters Corpus Volume 1) dataset is a large collection of over 800,000 newswire stories published by Reuters between 1996–1997. Articles are labeled with topic codes and other metadata, making the corpus widely used for research in text classification, natural language processing (NLP), and information retrieval. Due to its scale and professional authorship, RCV1 serves as a benchmark for studying stylistic and topical variation in human-written news text.

## Reuters 50/50 Description
The Reuters-50/50 dataset is a curated subset of RCV1 consisting of 5,000 documents evenly distributed across 50 authors (100 documents per author). Each author’s contribution is split into a training set (50 texts) and a test set (50 texts). The dataset is frequently used for authorship attribution, stylometric analysis, and exploratory text studies, as it controls for both topic diversity and author balance while remaining small enough to be computationally manageable.

## \_sp documents
These were cleaned of spelling errors using MS word and some elbow grease.  First, I created a singular file with a bash script like:
    for FILE in $(find . -name "*txt"); do
        echo $FILE >> CORPUS.doc
        cat $FILE >> CORPUS.doc
        printf "\n\n" >> CORPUS.doc
    done

Then, I then ran the spell checker to fix spelling mistakes, and British spelling.

Finally, I used disassemble_corpus_sp.py to put the documents back to individual files.