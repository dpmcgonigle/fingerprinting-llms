#   Scoring Text

##  Description
"Scoring" in this sense is getting the log probabilities for a text document.  I found that I was able to get all of the log probabilities for a given text document with the following parameters:

```python
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
```

Note that there are typically two logprobs that are "returned" at each token, the highest probability (top K where K=1) token, and the actual token used.  If the token used is the highest probability token, there is just the one.  So we just have to take max(rank) to get the actual input token.  

## score_text.py
I have created a python script that demonstrates this, and I have tested it on both the 8B and 70B quantized llama 3.1 models.  See Examples below for output:

##  Examples
```bash
(base) dma0523@str-mac-5442:fingerprinting-llms$ python scripts/score_text.py         -t data/rcv1-uc-irvine-subset/reuter5050/C50train/AaronPressman/401260newsML.txt         -m /disk1/dma0523/models/llama3.1-8b-w4a16 -p 8765

Loaded text : The Commodity Futures Trading Commission, one of the nation's primary regulators of derivatives, has...ying the case, the court suggested "these arguments are addressed to the Congress, not the courts."

choice = dict_keys(['index', 'text', 'logprobs', 'finish_reason', 'stop_reason', 'token_ids', 'prompt_logprobs', 'prompt_token_ids'])
Response text : The Commodity Futures Trading Commission, one of the nation's primary regulators of derivatives, has...
Token String, Token ID, Rank, LogProb
LPs : [None, ('The', 791, 72, -7.208318710327148), (' Com', 1219, 511, -8.181428909301758), ('modity', 52302, 5, -3.2642858028411865), (' Futures', 77367, 1, -0.43411555886268616), (' Trading', 32704, 1, -0.01882905885577202), (' Commission', 9849, 1, -0.0012024560710415244), (',', 11, 6, -5.341109752655029), (' one', 832, 26, -6.733638286590576), (' of', 315, 1, -0.005708463490009308), (' the', 279, 1, -0.08415645360946655), (' nation', 7140, 32, -5.582569122314453), ("'s", 596, 1, -0.3548031747341156), (' primary', 6156, 5, -3.583995819091797), (' regulators', 40242, 1, -0.4011480510234833), (' of', 315, 1, -0.21255068480968475), (' derivatives', 43645, 2, -2.062927007675171), (',', 11, 1, -0.991132915019989), (' has', 706, 1, -1.1857060194015503), (' no', 912, 78, -6.227603435516357)]
...
...[(' underlying', 16940, 15, -4.741006374359131), (' the', 279, 1, -0.14257575571537018), (' case', 1162, 1, -0.33949512243270874), (',', 11, 1, -0.025820661336183548), (' the', 279, 1, -0.8942029476165771), (' court', 5590, 2, -1.3243346214294434), (' suggested', 12090, 4, -2.6858301162719727), (' "', 330, 5, -4.1182379722595215), ('these', 45010, 38, -7.141630172729492), (' arguments', 6105, 39, -6.146756172180176), (' are', 527, 2, -1.8128089904785156), (' addressed', 20669, 48, -7.068564414978027), (' to', 311, 1, -0.8128992319107056), (' the', 279, 2, -1.0376551151275635), (' Congress', 8151, 2, -1.78339421749115), (',', 11, 1, -0.7414510250091553), (' not', 539, 1, -0.5306301116943359), (' the', 279, 2, -1.222027063369751), (' courts', 19359, 1, -0.21286562085151672), ('."\n', 10246, 2, -1.145362138748169)]
Returned text matches input text!!
```

```bash
(base) fingerprinting-llms$ python scripts/score_text.py         -t data/rcv1-uc-irvine-subset/reuter5050/C50train/AaronPressman/407599newsML.txt         -m /disk2/dma0523/models/llama3.1-70b-w4a16 -p 9000

Loaded text : Legislators introduced two bills Thursday to overturn the Clinton administration's export limits on ...Berman, who strongly opposes mandatory key recovery, said the policy ought to be "my lock, my key."

choice = dict_keys(['index', 'text', 'logprobs', 'finish_reason', 'stop_reason', 'token_ids', 'prompt_logprobs', 'prompt_token_ids'])
Response text : Legislators introduced two bills Thursday to overturn the Clinton administration's export limits on ...
Token String, Token ID, Rank, LogProb
LPs : [None, ('Leg', 19444, 960, -9.278214454650879), ('isl', 23265, 28, -6.00516939163208), ('ators', 3046, 2, -1.572616696357727), (' introduced', 11784, 94, -6.3672285079956055), (' two', 1403, 6, -3.3895533084869385), (' bills', 19123, 1, -0.7025643587112427), (' Thursday', 7950, 8, -4.060480117797852), (' to', 311, 3, -1.6135964393615723), (' overturn', 67687, 120, -7.065767288208008), (' the', 279, 1, -0.9642595052719116), (' Clinton', 8283, 655, -9.322127342224121), (' administration', 8735, 1, -0.39642342925071716), ("'s", 596, 1, -0.233351469039917), (' export', 7637, 433, -9.149590492248535), (' limits', 13693, 16, -5.847190856933594), (' on', 389, 1, -0.034722112119197845), (' computer', 6500, 4, -3.119746446609497), (' encryption', 26542, 3, -1.9471518993377686), (' technology', 5557, 1, -0.6513236165046692)]
...
...[(' who', 889, 2, -1.683496356010437), (' strongly', 16917, 113, -7.325534343719482), (' opposes', 76312, 2, -1.5848150253295898), (' mandatory', 23911, 1, -0.853290319442749), (' key', 1401, 1, -0.015276335179805756), (' recovery', 13654, 1, -0.026703285053372383), (',', 11, 1, -0.11798646301031113), (' said', 1071, 1, -0.6928110718727112), (' the', 279, 1, -1.1059035062789917), (' policy', 4947, 33, -5.625795364379883), (' ought', 22525, 855, -10.525851249694824), (' to', 311, 1, -0.12647193670272827), (' be', 387, 1, -0.19744214415550232), (' "', 330, 1, -2.9490132331848145), ('my', 2465, 1077, -9.959330558776855), (' lock', 5409, 8, -3.944516181945801), (',', 11, 1, -0.08662460744380951), (' my', 856, 1, -0.01105104386806488), (' key', 1401, 1, -0.045799627900123596), ('."\n', 10246, 5, -2.423306941986084)]
Returned text matches input text!!
```