#   Prompting

##  Description
In order to create the LLM-generated corpus, we're going to need to come up 

## Initial Prompt
You are an experienced Reuters business and finance reporter. 
Your writing follows Reuters style: concise, factual, third-person, and neutral in tone. 
You write short newswire stories suitable for immediate publication, using the inverted-pyramid structure 
(lead sentence summarizing the news, followed by supporting context, background, and one or two quotes or data points).

Your task:
- Read the sample newswire text below.
- Identify the key entities (companies, people, or organizations) mentioned.
- Write a different news story in the same domain (business/finance) that still involves these entities, 
  but describes a new or hypothetical event.
- Use typical American English.
- Do not copy or paraphrase sentences from the original. 
  Invent a plausible but distinct story consistent with real-world reporting.
- Keep the tone journalistic, objective, and Reuters-like.
- Aim for about 500 words, with about 20-25 words per sentence.  It is fine to deviate from this, this is just a target.

Return only the new article text, without commentary or headings.

Newswire source:
"""
{{newswire_text}}
"""

##  Scripts

### Llama

```bash
for FILEPATH in $(find data/rcv1-uc-irvine-subset/reuter5050/C50train_clean/ -name "*.txt"); do bash scripts/chat.sh -p 9003 -mp "/disk2/dma0523/models/llama3.1-70b-w4a16" -o ${FILEPATH/rcv1-uc-irvine-subset/llama70Bw4a16} -m 'You are an experienced Reuters business and finance reporter. 
Your writing follows Reuters style: concise, factual, third-person, and neutral in tone. 
You write short newswire stories suitable for immediate publication, using the inverted-pyramid structure 
(lead sentence summarizing the news, followed by supporting context, background, and one or two quotes or data points).

Your task:
- Read the sample newswire text below.
- Identify ALL of the key entities (companies, people, or organizations) mentioned, and use those in your story.
- Write a different news story in the same domain (business/finance) that still involves ALL of the key entities mentioned earlier, 
  but describes a new or hypothetical event.
- Use typical American English. 
- These stories are from the 1990s, so please do not violate this by talking about anything outside of that era.
- Do not copy or paraphrase sentences from the original. 
  Invent a plausible but distinct story consistent with real-world reporting.
- Keep the tone journalistic, objective, and Reuters-like.
- Aim for about 500 words, with about 20-25 words per sentence.  It is fine to deviate from this, this is just a target.

Return only the new article text, without commentary or headings.

Newswire source: \n'"$(cat $FILEPATH)"; printf "\n\n"; done
```

### Mixtral
```bash
for FILEPATH in $(find data/rcv1-uc-irvine-subset/reuter5050/C50train_clean/ -name "*.txt"); do bash scripts/chat.sh -p 9999 -mp "/proj/redline/team/mcg/models/Mixtral-8x7B-Instruct-v0.1" -o ${FILEPATH/rcv1-uc-irvine-subset/mixtral-8x7B-instruct} -m 'You are an experienced Reuters business and finance reporter. 
Your writing follows Reuters style: concise, factual, third-person, and neutral in tone. 
You write short newswire stories suitable for immediate publication, using the inverted-pyramid structure 
(lead sentence summarizing the news, followed by supporting context, background, and one or two quotes or data points).

Your task:
- Read the sample newswire text below.
- Identify ALL of the key entities (companies, people, or organizations) mentioned, and use those in your story.
- Write a different news story in the same domain (business/finance) that still involves ALL of the key entities mentioned earlier, 
  but describes a new or hypothetical event.
- Use typical American English. 
- These stories are from the 1990s, so please do not violate this by talking about anything outside of that era.
- Do not copy or paraphrase sentences from the original. 
  Invent a plausible but distinct story consistent with real-world reporting.
- Keep the tone journalistic, objective, and Reuters-like.
- Aim for about 500 words, with about 20-25 words per sentence.  It is fine to deviate from this, this is just a target.

Return only the new article text, without commentary or headings.

Newswire source: \n'"$(cat $FILEPATH)"; printf "\n\n"; done
```

##  TODO: 10/19/2025
I stopped short of generating all 2500 LLM documents for the reuters5050 dataset for both Llama3.1-8b-w4a16 and Mixtral-8x7B-Instruct-v0.1.  Left TODO:

### Mixtral Completed (1027 files)
```bash
204K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/AaronPressman
208K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/DavidLawder
204K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/EdnaFernandes
200K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/EricAuchard
208K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/JanLopatka
200K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/JoeOrtiz
200K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/JohnMastrini
200K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/KarlPenhaul
200K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/KevinDrawbaugh
204K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/KevinMorrison
208K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/KouroshKarimkhany
200K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/LynneO'Donnell
204K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/LynnleyBrowning
204K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/MartinWolk
204K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/MichaelConnor
200K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/PatriciaCommins
196K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/RobinSidel
204K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/SamuelPerry
200K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/ScottHillis
200K	data/mixtral-8x7B-instruct/reuter5050/C50train_clean/SimonCowell
```

### Llama Completed (1733 files)
```bash
200K	data/llama70Bw4a16/reuter5050/C50train_clean/AaronPressman
200K	data/llama70Bw4a16/reuter5050/C50train_clean/AlanCrosby
200K	data/llama70Bw4a16/reuter5050/C50train_clean/AlexanderSmith
200K	data/llama70Bw4a16/reuter5050/C50train_clean/BenjaminKangLim
200K	data/llama70Bw4a16/reuter5050/C50train_clean/BernardHickey
192K	data/llama70Bw4a16/reuter5050/C50train_clean/BradDorfman
200K	data/llama70Bw4a16/reuter5050/C50train_clean/DarrenSchuettler
200K	data/llama70Bw4a16/reuter5050/C50train_clean/DavidLawder
200K	data/llama70Bw4a16/reuter5050/C50train_clean/EdnaFernandes
200K	data/llama70Bw4a16/reuter5050/C50train_clean/EricAuchard
200K	data/llama70Bw4a16/reuter5050/C50train_clean/FumikoFujisaki
200K	data/llama70Bw4a16/reuter5050/C50train_clean/GrahamEarnshaw
200K	data/llama70Bw4a16/reuter5050/C50train_clean/HeatherScoffield
200K	data/llama70Bw4a16/reuter5050/C50train_clean/JaneMacartney
200K	data/llama70Bw4a16/reuter5050/C50train_clean/JanLopatka
196K	data/llama70Bw4a16/reuter5050/C50train_clean/JimGilchrist
200K	data/llama70Bw4a16/reuter5050/C50train_clean/JoeOrtiz
200K	data/llama70Bw4a16/reuter5050/C50train_clean/JohnMastrini
200K	data/llama70Bw4a16/reuter5050/C50train_clean/JonathanBirt
200K	data/llama70Bw4a16/reuter5050/C50train_clean/JoWinterbottom
200K	data/llama70Bw4a16/reuter5050/C50train_clean/KarlPenhaul
200K	data/llama70Bw4a16/reuter5050/C50train_clean/KeithWeir
200K	data/llama70Bw4a16/reuter5050/C50train_clean/KevinDrawbaugh
200K	data/llama70Bw4a16/reuter5050/C50train_clean/KevinMorrison
200K	data/llama70Bw4a16/reuter5050/C50train_clean/KouroshKarimkhany
200K	data/llama70Bw4a16/reuter5050/C50train_clean/LynneO'Donnell
200K	data/llama70Bw4a16/reuter5050/C50train_clean/LynnleyBrowning
200K	data/llama70Bw4a16/reuter5050/C50train_clean/MartinWolk
200K	data/llama70Bw4a16/reuter5050/C50train_clean/MichaelConnor
200K	data/llama70Bw4a16/reuter5050/C50train_clean/PatriciaCommins
196K	data/llama70Bw4a16/reuter5050/C50train_clean/RobinSidel
200K	data/llama70Bw4a16/reuter5050/C50train_clean/SamuelPerry
200K	data/llama70Bw4a16/reuter5050/C50train_clean/ScottHillis
200K	data/llama70Bw4a16/reuter5050/C50train_clean/SimonCowell
```