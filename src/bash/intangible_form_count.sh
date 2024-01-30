#!/bin/bash
src_dir="${1:-}"
dest_dir="${2:-}"


start_file=$(cat progress.txt)

num_files=2

end_file=$((start_file + num_files))
echo $end_file > progress.txt

venv/bin/python src/html_processor/retrive_intangible_table.py  $src_dir $dest_dir $start_file  $num_files