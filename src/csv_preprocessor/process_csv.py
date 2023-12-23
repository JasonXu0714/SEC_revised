import pandas as pd
import numpy as np
import os
import sys

sys.path.append("/Users/yanzhe.li/Documents/sec_webscraping/src")
import config
import export_dataframe


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


def csv_runner(csv_dir, keywords):
    all_csv_files = os.listdir(csv_dir)
    for file in all_csv_files:
        df = pd.read_csv(os.path.join(csv_dir, file))
        result_df = extract_intangile_form(df, keywords)
        result_df.to_csv(
            f"/Users/yanzhe.li/Documents/sec_webscraping/data/extracted_csv/{file}"
        )


def extract_intangile_form(original_df, keywords):
    original_df.loc[:, keywords] = original_df.apply(get_first_number, axis=1)
    reduced_df = original_df.dropna(subset=keywords)
    # slice only the first column and the new created one
    return reduced_df.iloc[:, [0]].join(reduced_df[keywords])


if __name__ == "__main__":
    data_dir = "/Users/yanzhe.li/Documents/sec_webscraping/data"
    target_dir = "test"
    csv_dir = os.path.join(data_dir, target_dir)
    keywords = config.Intangible_keywords
    csv_runner(csv_dir, keywords)
