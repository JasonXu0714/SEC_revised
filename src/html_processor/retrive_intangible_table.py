import pandas as pd
import polars as pl
import src.secret_finder as secret_finder
import src.export_dataframe as export_dataframe
import os
import multiprocessing


import config

keywords = config.Intangible_keywords


def html_runner(html_dir):
    html_files = os.listdir(html_dir)
    p = multiprocessing.Pool()
    p.starmap(read_html_file, [(html_dir, filename) for filename in html_files])


def read_html_file(html_dir, filename):
    try:
        list_df = pd.read_html(os.path.join(html_dir, filename))
    except ValueError as e:
        print(e)
    process_list_df(list_df, filename)


def process_list_df(list_df, file_name):
    for form_df in list_df:
        texts = form_df.to_markdown()
        find_match = secret_finder.find_secret(keywords, texts)
        if find_match:
            export_dataframe.output_to_csv(
                form_df,
                data_path=os.path.join(config.root_directory, "data"),
                folder="test_intangible",
                filename=file_name.replace("txt", "csv"),
            )


if __name__ == "__main__":
    root_directory = config.root_directory
    data_dir = os.path.join(root_directory, "data")
    target_dir = "first_html"
    html_dir = os.path.join(data_dir, target_dir)
    html_runner(html_dir)
