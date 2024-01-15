import pandas as pd
import polars as pl
import src.secret_finder as secret_finder
import src.export_dataframe as export_dataframe
import os
import sys
import multiprocessing
from src.time.timer import Timer


import config

keywords = config.Intangible_keywords


def html_runner(html_dir, output_folder):
    html_files = os.listdir(html_dir)
    p = multiprocessing.Pool()
    p.starmap(
        read_html_file, [(html_dir, output_folder, filename) for filename in html_files]
    )


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
    for form_df in list_df:
        texts = form_df.to_markdown()
        find_match = secret_finder.find_secret(keywords, texts)
        if find_match:
            export_dataframe.output_to_csv(
                form_df,
                folder=output_folder,
                filename=file_name.replace("txt", "csv"),
            )


if __name__ == "__main__":
    timer = Timer()
    timer.start()
    root_directory = config.root_directory
    data_dir = os.path.join(root_directory, "data")
    src_dir, dest_dir = sys.argv[1:]
    html_dir = os.path.join(data_dir, src_dir)
    html_runner(html_dir, output_folder=dest_dir)
    timer.stop()
    print(f"Elapsed time: {timer.elapsed_time()} seconds")
