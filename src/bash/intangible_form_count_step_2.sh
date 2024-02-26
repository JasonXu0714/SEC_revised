#!/bin/bash
src_dir="${1:-}"
dest_dir="${2:-}"


start_file=$(cat progress.txt)

num_files=1000000

end_file=$((start_file + num_files))
echo $end_file > progress.txt

venv/bin/python src/csv_preprocessor/process_csv.py  $src_dir $dest_dir $start_file  $num_files
