#   Dataset Considerations

##  Description
This document is meant to serve as an aid in deciding on which dataset to use for my main focus of this project.

### Considerations
My priorities and concerns are the following: 
1. Obtaining a "signal" (aspirationally-) free from domain-specific noise, meaning that differences in the signal come from styles associated with general English language patterns and not from domain-specific jargon and idiosyncrasies. 
2. Being able to sufficiently clean the dataset of noise that I don't want to contribute to the signal. This noise includes, but is not limited to: 
    2.1. Spelling and egregious grammatical mistakes -- I want to assume "highly competent" writers who know how to use spell checkers 
    2.2. Names and technical jargon 
    2.3. Unnecessary structural components like bibliography of table of contents. Some structure, like intro->body->conclusion, (or something different in the news articles that involves attention-grabbing lines, etc) is fine. 
3. Being able to create repeatable prompts that will generate analogous LLM-generated texts. I don't want to lead the LLM into "write the same story", but I'd like to create a corpus of very similar documents. I'm considering using an LLM to extract key points like subject matter, and creating a prompt from that can create a similar, but not identical, document.

##  Decision - Reuters 50/50
I think Reuters-50/50 fits the criteria well based on the following

### Signal with minimal domain-specific noise
- All texts belong to a single topic Corporate / Industrial news class (CCAT in orig. RCV1), reducing content variation across documents.
- Consistent grammar and style keeps the distribution tighter and more well-defined.

### Cleanability and noise control
- Structural components like headers and metadata (bylines, datelines) are more regular and easily handled.
- Named entities can be masked with NER tools to suppress topic leakage.
- Narrower domain makes for less "unknown unknowns".

### Repeatable LLM prompting
- We should be able to make stable prompt templates due to the consistent structures “fact-sheet → rewrite” workflows.
- We have a balanced author set that should make for some stylistic stability.

##  Additional Considerations

### Drawbacks of Reuters 50/50
- Articles are significantly shorter, which may make the problem more challenging.
- Strong stylistic conventions will make it difficult to separate domain-specific signal from general English language patterns.
- Boilerplate artifacts may also be a significant challenge due to the nature of newswire.

### Considerations for Data Prep
We may be able to mitigate some of those problems by
- Strict boilerplate stripping
- NER masking plus careful reinsertion of neutral placeholders
- Controlling for length within some tolerance
- per-author stratified splits
- Stretch goal: We may be able to create a good cross-register validation set from a single-genre slice of MICUSP to test generalization down the road.