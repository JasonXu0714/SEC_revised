import pandas as pd
import numpy as np
import os
import sys

# add src to sys path and import customize package
pwd = os.getcwd()
root_directory = os.path.abspath(os.path.join(pwd, "../../"))
sys.path.append(root_directory)
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


def csv_runner(csv_dir, data_dir, folder="extracted_csv"):
    all_csv_files = os.listdir(csv_dir)
    for file in all_csv_files:
        df = pd.read_csv(os.path.join(csv_dir, file))
        result_df = extract_intangile_form(df)
        export_dataframe.output_to_csv(
            result_df, data_dir, folder=folder, filename=file
        )


def extract_intangile_form(original_df, intangible_col="intangible asset value"):
    original_df[intangible_col] = original_df.apply(get_first_number, axis=1)
    reduced_df = original_df.dropna(subset=intangible_col)
    # slice only the first column and the new created one
    return reduced_df.iloc[:, [0]].join(reduced_df[intangible_col])


if __name__ == "__main__":
    current_dir = os.getcwd()
    root_directory = os.path.abspath(os.path.join(current_dir, "../.."))
    data_dir = os.path.join(root_directory, "data")
    # test/intangible dir
    target_dir = "test"
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]

    csv_dir = os.path.join(data_dir, target_dir)
    keywords = config.Intangible_keywords
    csv_runner(csv_dir, data_dir)
