#   Issues

##  Description
This is just a place to document specific issues I've run into

##  Mixtral whitespace issue (12/01/2025)
It appears that the Mixtral documents all start with a space, which adds a very, very low probability token to start with.

##  Integer out of bounds
My token ranks is currently using int16, but it seems like the size of the vocabulary exceeds that:

```bash
Traceback (most recent call last):
  File "/Users/dma0523/code/math/fingerprinting-llms/scripts/score_text.py", line 106, in <module>
    main(args)
  File "/Users/dma0523/code/math/fingerprinting-llms/scripts/score_text.py", line 99, in main
    score_doc(server=server, model=args.model, input_filepath=args.input_filepath, output_filepath=args.output_filepath)
  File "/Users/dma0523/code/math/fingerprinting-llms/scripts/score_text.py", line 78, in score_doc
    logprobs: LogProbs = extract_prompt_logprobs(
                         ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/envs/llm-fp/lib/python3.12/site-packages/fingerprinting_llms/score/extract.py", line 87, in extract_prompt_logprobs
    log_probs = LogProbs.from_lists(
                ^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/envs/llm-fp/lib/python3.12/site-packages/fingerprinting_llms/score/__init__.py", line 36, in from_lists
    arr_ranks = np.asarray(token_ranks, dtype=np.int16)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
OverflowError: Python integer 55705 out of bounds for int16
```

Note that this appears to be exceedingly rare (I ran into it once in scoring 100 files, I think).

### 11/21/2025 -- I ran into this consistently now
When grading Mixtral-generated docs with Llama, I'm getting this consistently, so I decided to bump up to int32

##  Mixtral-8x7B-Instruct-v0.1-AWQ failure
I wasn't able to get this working.  I troubleshot it for a while and then gave up, using Mixtral-8x7B-Instruct-v0.1 for the "secondary LLM".