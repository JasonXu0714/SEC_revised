import argparse
import pandas as pd
import src.secret_finder as secret_finder
import src.export_dataframe as export_dataframe
import os
import sys
import multiprocessing
import config
from tqdm import tqdm
from src.time.timer import Timer

keywords = config.Intangible_keywords


def html_runner(html_dir, output_folder, start_file, max_file=4):
    """
    Input:
        html_dir:directory to store raw html file
        output_folder:csv file transformed from html file with key words
        max_file: num of files to process each time
    """

    all_html_files = os.listdir(html_dir)
    html_files = all_html_files[start_file : start_file + max_file + 1]
    p = multiprocessing.Pool()
    with tqdm(total=len(html_files)) as progress_bar:
        for _ in p.starmap(
            read_html_file,
            [(html_dir, output_folder, filename) for filename in html_files],
        ):
            progress_bar.update(1)


def read_html_file(html_dir, output_folder, filename):
    try:
        list_df = pd.read_html(os.path.join(html_dir, filename))
    except ValueError as e:
        print(e)
        return
    process_list_df(list_df, output_folder, filename)


def process_list_df(
    list_df,
    output_folder,
    file_name,
):
    form_number = 0
    for form_df in list_df:
        texts = form_df.to_markdown()
        find_match = secret_finder.find_secret(keywords, texts)
        if find_match:
            file_name_without_extension = file_name.split(".")[0]
            file_name_with_index = file_name_without_extension + f"_{form_number}.csv"
            export_dataframe.output_to_csv(
                form_df,
                folder=output_folder,
                filename=file_name_with_index,
            )
            form_number += 1


if __name__ == "__main__":
    timer = Timer()
    timer.start()
    root_directory = config.root_directory
    data_dir = os.path.join(root_directory, "data")
    print(sys.argv[1:])
    src_dir, dest_dir, start_file, numOfFiles = sys.argv[1:]

    html_dir = os.path.join(data_dir, src_dir)

    html_runner(
        html_dir,
        output_folder=dest_dir,
        start_file=int(start_file),
        max_file=int(numOfFiles),
    )
    timer.stop()
    print(f"Elapsed time: {timer.elapsed_time()} seconds")
