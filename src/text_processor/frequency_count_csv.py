import os
import config
import pandas as pd
import sys
import src.export_dataframe as export_dataframe
import multiprocessing
from frequency_count import *


def frequency_count_dataframe(df):
    """
    Input: dataframe of each intangible form
    Output: array of tuple(word,occurrence)
    """
    word_filtered = df.iloc[:, 0].apply(filter_words)
    grams = word_filtered.apply(produce_grams)
    grams = [item for sublist in grams for item in sublist]
    return Counter(map(str.lower, grams))


def frequency_count_runner(csv_dir, columns, folder="frequency_count"):
    """
    Input:Dir of extracted csv
    Output: list -> dataframe -> csv
    """
    # all_csv_files = os.listdir(csv_dir)
    # for file in all_csv_files:
    #     df = pd.read_csv(os.path.join(csv_dir, file))
    #     count_dict = frequency_count_dataframe(df)
    #     if not count_dict:
    #         continue
    #     result_df = pd.DataFrame.from_dict(count_dict, orient="index").reset_index()
    #     result_df.columns = columns
    #     export_dataframe.output_to_csv(result_df, folder=folder, filename=file)
    csv_files = os.listdir(csv_dir)
    p = multiprocessing.Pool()
    p.starmap(
        frequency_count_each_file,
        [(csv_dir, columns, folder, filename) for filename in csv_files],
    )


def frequency_count_each_file(csv_dir, columns, folder, filename):
    df = pd.read_csv(os.path.join(csv_dir, filename))
    count_dict = frequency_count_dataframe(df)
    if count_dict:
        result_df = pd.DataFrame.from_dict(count_dict, orient="index").reset_index()
        result_df.columns = columns
        export_dataframe.output_to_csv(result_df, folder=folder, filename=filename)


if __name__ == "__main__":
    columns = ["word", "count"]
    root_directory = config.root_directory
    data_dir = os.path.join(root_directory, "data")
    src_dir, dest_dir = sys.argv[1:]
    csv_dir = os.path.join(data_dir, src_dir)
    frequency_count_runner(csv_dir, columns=columns, folder=dest_dir)
