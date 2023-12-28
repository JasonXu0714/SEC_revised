SHELL := /bin/bash
export PYTHONPATH := $(shell pwd)
.PHONY: all setup pull_intangible_form process_csv clean
DARA_DIRS=attchment csv_to_extract extracted_csv frequency_count frequency_merged intangible test test_count test_merge

setup:
	@echo "Moving to main branch"
	git switch main
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	@echo "Installing requirements..."
	venv/bin/pip install -r requirements.txt
creat_dir:
	@echo "Creating data sub directory if not existed..."
	mkdir -p $(addprefix data/,$(DARA_DIRS))
pull_intangible_form:
	echo "Running script to pull forms containing intangible asset ..."
	venv/bin/python src/main_refactor.py

process_csv:
	echo "Extracting numerical records related with intangible assets"
	venv/bin/python src/csv_preprocessor/process_csv.py "intangible"
csv_word_count:
	venv/bin/python src/text_processor/frequency_count_csv.py  "extracted_csv"
merge_frequency_count:
	venv/bin/python src/csv_preprocessor/merge_frequency_count.py "frequency_count"
clean:
	@echo "Cleaning up..."
	@echo "Removing virtual environment..."
	rm -rf venv