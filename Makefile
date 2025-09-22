# 	Makefile for common project tasks

.PHONY: format lint type test build clean lock-cpu lock-gpu update-cpu update-gpu

#	Environment Creation Tasks
lock-cpu:
	conda-lock lock \
		-f env/environment.base.yml \
		-p osx-arm64 -p osx-64 -p linux-64 -p win-64 \
		--lockfile conda-lock.cpu.conda-lock.yml

lock-gpu:
	conda-lock lock \
		-f env/environment.base.yml \
		-f env/environment.gpu.cuda121.yml \
		-p linux-64 -p win-64 \
		--lockfile conda-lock.gpu.cuda121.conda-lock.yml

update-cpu:
	conda-lock install --name llm-fp conda-lock.cpu.conda-lock.yml

update-gpu:
	conda-lock install --name llm-fp conda-lock.gpu.cuda121.conda-lock.yml

#	Development Tasks
format:
	black .
	ruff check --fix .

lint:
	ruff check .

type:
	mypy fingerprinting_llms

test:
	pytest

#	Packaging Tasks
build:
	python -m build

clean:
	rm -rf dist build *.egg-info .pytest_cache .mypy_cache .ruff_cache
