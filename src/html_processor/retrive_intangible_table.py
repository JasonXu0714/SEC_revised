import pandas as pd
import polars as pl
import src.secret_finder as secret_finder
import src.export_dataframe as export_dataframe
import os


import config

keywords = config.Intangible_keywords


def read_html_file(html_dir):
    html_files = os.listdir(html_dir)
    for html_file in html_files:
        try:
            list_df = pd.read_html(os.path.join(html_dir, html_file))
        except ValueError as e:
            print(e)
            continue
        process_list_df(list_df, html_file)


def process_list_df(list_df, file_name):
    for form_df in list_df:
        texts = form_df.to_markdown()
        find_match = secret_finder.find_secret(keywords, texts)
        if find_match:
            export_dataframe.output_to_csv(
                form_df,
                data_path=os.path.join(config.root_directory, "data"),
                folder="intangible_local",
                filename=file_name.replace("txt", "csv"),
            )


if __name__ == "__main__":
    root_directory = config.root_directory
    data_dir = os.path.join(root_directory, "data")
    target_dir = "first_html"
    html_dir = os.path.join(data_dir, target_dir)
    read_html_file(html_dir)
