import pandas as pd
import numpy as np
import os
import sys
import multiprocessing
import config
import src.export_dataframe as export_dataframe


def is_number(s):
    try:
        if float(s) > 0:
            return float(s)
    except ValueError:
        return False


def get_first_number(series):
    for value in series.values:
        if is_number(value):
            return is_number(value)
    return np.nan


def csv_runner(csv_dir, output_folder="extracted_csv"):
    all_csv_files = os.listdir(csv_dir)
    p = multiprocessing.Pool()
    p.starmap(
        csv_reader_writer,
        [(csv_dir, output_folder, filename) for filename in all_csv_files],
    )


def csv_reader_writer(csv_dir, output_folder, filename):
    try:
        df = pd.read_csv(os.path.join(csv_dir, filename))
        result_df = extract_intangile_form(df)
        export_dataframe.output_to_csv(
            result_df, folder=output_folder, filename=filename
        )
    except (IOError, ValueError) as e:
        print(e)


def extract_intangile_form(original_df, intangible_col="intangible asset value"):
    original_df[intangible_col] = original_df.apply(get_first_number, axis=1)
    reduced_df = original_df.dropna(subset=intangible_col)
    # slice only the first column and the new created one
    return reduced_df.iloc[:, [0]].join(reduced_df[intangible_col])


if __name__ == "__main__":
    root_directory = config.root_directory
    data_dir = os.path.join(root_directory, "data")
    src_dir, dest_dir = sys.argv[1:]
    csv_dir = os.path.join(data_dir, src_dir)
    csv_runner(csv_dir, output_folder=dest_dir)
