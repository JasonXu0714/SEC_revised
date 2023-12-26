SHELL := /bin/bash
export PYTHONPATH := $(shell pwd)
.PHONY: all setup pull_intangible_form process_csv clean

all: setup pull_intangible_form process_csv clean
run_all: setup process_csv csv_word_count clean
setup:
	@echo "Moving to main branch"
	git switch main
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	@echo "Installing requirements..."
	venv/bin/pip install -r requirements.txt

pull_intangible_form:
	echo "Running script to pull forms containing intangible asset ..."
	venv/bin/python src/main_refactor.py

process_csv:
	echo "Extracting numerical records related with intangible assets"
	venv/bin/python src/csv_preprocessor/process_csv.py "intangible"
csv_word_count:
	venv/bin/python src/text_processor/frequency_count_csv.py  "extracted_csv"
clean:
	@echo "Cleaning up..."
	@echo "Removing virtual environment..."
	rm -rf venv