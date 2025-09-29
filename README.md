#   Fingerprinting LLMs

##  Contents
- [Project Description](#project-description)
- [Project Documentation](#project-documentation)
- [Installation](#installation)
    - [Environment](#environment)
    - [llm-fingerprinting](#llm-fingerprinting)
- [Data](#data)
    - [Reuters 5050 Subset](#reuters-5050-subset)

## Project Description
This project explores methods to **fingerprint large language models (LLMs)** by analyzing statistical and structural properties of generated text.  This is a project for the Mathematics Senior Seminar at UML.

The aim is twofold:
1. **Detection** — distinguish LLM-generated text from human-written text.  
2. **Attribution** — identify which LLM may have produced a given text sample.

The approach combines techniques from **stylometry, information theory, and signal processing** identify patterns that are subtle for humans but systematic for models.

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
The dataset is

### Reuters 5050 Subset
Description and data in rcv1-uc-irvine-subset (data not currently stored in repository).

[Back to Top](#fingerprinting-llms)

---

## TODO: Finish README
