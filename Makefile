SHELL := /bin/bash
export PYTHONPATH := $(shell pwd)

.PHONY: all setup creat_dir pull_intangible_form process_csv csv_word_count merge_frequency_count clean
DARA_DIRS= raw_data intangible_local attchment csv_to_extract extracted_csv frequency_count frequency_merged intangible test test_count test_merge

move_file:
	bash src/bash/move_file.sh "test" "test/test_output"

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
# pull_intangible_form:
# 	echo "Running script to pull forms containing intangible asset ..."
# 	bash src/bash/intangible_form_count.sh "first_html" "intangible_local"
pull_intangible_form:
	@echo "Running script to pull forms containing intangible asset ..."
	@venv/bin/python  src/html_processor/retrive_intangible_table_refactor.py "first_html_subsample" "test_intangible"
process_csv:
	echo "Extracting numerical records related with intangible assets"
	venv/bin/python src/csv_preprocessor/process_csv.py  "test_intangible" "keep_two_column_intangible_test"
csv_word_count:
	venv/bin/python src/text_processor/frequency_count_csv.py "keep_two_column_intangible_test" "test_count" 
merge_frequency_count:
	venv/bin/python src/csv_preprocessor/merge_frequency_count.py  "test_count" "test_merge"
clean test_dirs:

clean:
	@echo "Cleaning up..."
	@echo "Removing virtual environment..."
	rm -rf venv
