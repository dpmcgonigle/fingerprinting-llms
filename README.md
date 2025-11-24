#   Fingerprinting LLMs

##  Contents
- [Project Description](#project-description)
- [Project Documentation](#project-documentation)
- [Notebooks](#notebooks)
    - [EDA-Stylometric](#eda-stylometric)
    - [EDA-LogProbs](#eda-logprobs)
    - [Burstiness-Author](#burstiness-author)
    - [Burstiness-AllReuters](#burstiness-allreuters)
    - [Burstiness-*DeepDive](#burstiness-deepdive)
- [Installation](#installation)
    - [Environment](#environment)
    - [llm-fingerprinting](#llm-fingerprinting)
- [Data](#data)
    - [Reuters 5050 Subset](#reuters-5050-subset)
    - [Reuters 5050 Subset](#reuters-5050-subset)

## Project Description
This project explores methods to **fingerprint large language models (LLMs)** by analyzing statistical and structural properties of generated text.  This is a project for the Mathematics Senior Seminar at UML.

The aim is twofold:
1. **Detection** — distinguish LLM-generated text from human-written text.  
2. **Attribution** — identify which LLM may have produced a given text sample.

The approach combines techniques from **stylometry, information theory, and signal processing** identify patterns that are subtle for humans but systematic for models.

[Back to Top](#fingerprinting-llms)

## Notebooks

This project contains various Jupyter notebooks organized into categories for different analysis stages:

### EDA-Stylometric

Exploratory Data Analysis focused on stylometric features of text. These notebooks were used to determine the optimal dataset for our research and necessary text cleaning procedures. They analyze traditional stylometric markers such as sentence length, vocabulary richness, and grammatical patterns.

### EDA-LogProbs

Analysis of log probability distributions to assess how distinguishable human and LLM-generated text are. These notebooks explore whether there's any inherent bias when evaluating LLM-generated text using the same model that produced it, and how this might affect detection methods.

### Burstiness-Author

Investigation of spectral and statistical differences between authentic author works and synthetically generated content mimicking their style. These notebooks focus on identifying unique "fingerprints" that distinguish genuine author patterns from LLM imitations.

### Burstiness-AllReuters

Generalization experiments across the Reuters dataset to test the broader applicability of our fingerprinting methods:
- **v1**: Initial analysis using the original 7 core features from the Burstiness notebooks
- **v2**: Expanded feature set with significantly more metrics to improve detection accuracy

### Burstiness-DeepDive

Going deeper into the search space from the Burstiness-AllReuters notebooks for specific feature types.

### Burstiness-EventAnalysis

Looking at specific patterns of text as "events" to see if there is a detectable difference between human and LLM-generated content. 

### Burstiness-HC3

Expanding initial burstiness exploration into a new dataset -- HC3

[Back to Top](#fingerprinting-llms)

## Project Documentation
I will be keeping documentation for tracking project details, meetings, explanations and goals in docs/

[Back to Top](#fingerprinting-llms)

##  Installation

### Environment
To install the CPU-only version of the enrivonment:
`conda-lock install --name llm-fp conda-lock.cpu.conda-lock.yml`

To install the GPU-enabled (nvidia) version of the environment:
`conda-lock install --name llm-fp conda-lock.gpu.cuda121.conda-lock.yml`

### llm-fingerprinting
This is the repository that includes the `llm_fingerprinting` package.  You can install with development tools and editability like:

`python -m pip install -e ".[dev]"`

For a simple install:

`python -m pip install .`

[Back to Top](#fingerprinting-llms)

## Data

### Reuters 5050 Subset
Description and data in [rcv1-uc-irvine-subset README.md](data/rcv1-uc-irvine-subset/reuter5050/README.md).

### Human ChatGPT Comparison Corpus (HC3) Dataset
Description and data in [HC3 README.md](data/hc3/README.md).

[Back to Top](#fingerprinting-llms)

---

## TODO: Finish README
