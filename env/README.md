#   llm-fp environments

##  Description
This document contains instructions for creating environments, and creating the tools for environment creation.

##  Installation

### Create Dev Environment with CPU only 
`conda-lock install --name llm-fp conda-lock.cpu.conda-lock.yml`

### Create Dev Environment with GPU
`conda-lock install --name llm-fp conda-lock.gpu.cuda121.conda-lock.yml`

### Create VLLM Environment for serving models
```bash
conda create vllm-env python==3.11.0 -y
conda activate vllm-env
pip install -r vllm-requirements.txt
```

##  Lockfiles
These are used to provide exact reproducibility of Conda environments across different machines and over time.  These will need to be re-generated if the dependencies change.

### Lockfile Create Instructions

#### Install conda-lock once
`conda install -n base -c conda-forge conda-lock -y`

#### CPU lock (works for osx-64, osx-arm64, linux-64, win-64)
```bash
conda-lock lock \
  -f env/environment.base.yml \
  -p osx-arm64 -p osx-64 -p linux-64 -p win-64 \
  --lockfile conda-lock.cpu.conda-lock.yml
```

#### GPU lock (CUDA 12.1) — typically linux-64 and/or win-64
```bash
conda-lock lock \
  -f env/environment.base.yml \
  -f env/environment.gpu.cuda121.yml \
  -p linux-64 -p win-64 \
  --lockfile conda-lock.gpu.cuda121.conda-lock.yml
```
