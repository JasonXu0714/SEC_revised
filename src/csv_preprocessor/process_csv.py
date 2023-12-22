import pandas as pd
import numpy as np
import os
import sys

sys.path.append("/Users/yanzhe.li/Documents/finance/sec_clean/src")
import config
import export_dataframe


def is_number(s):
    try:
        float(s)
        return float(s)
    except ValueError:
        return False


def get_first_number(series):
    for item in series:
        if is_number(item):
            return is_number(item)
    return np.nan


def csv_runner(csv_dir, keywords):
    all_csv_files = os.listdir(csv_dir)
    for file in all_csv_files:
        df = pd.read_csv(os.path.join(csv_dir, file))
        result_df = extract_intangile_form(df, keywords)
        result_df.to_csv(
            f"/Users/yanzhe.li/Documents/finance/sec_clean/data/extracted_csv/{file}"
        )


# def filter_by_keywords(original_df, keywords):
#     # mask = original_df.iloc[:, 0].str.lower().isin(keywords)  # ??
#     mask = (
#         original_df.iloc[:, 0]
#         .astype(str)
#         .str.lower()
#         .apply(lambda x: any(keyword in x for keyword in keywords))
#     )
#     return original_df[mask]


def extract_intangile_form(original_df, keywords):
    original_df.loc[:, keywords] = original_df.apply(get_first_number, axis=1)
    reduced_df = original_df.dropna(subset=keywords)
    # slice only the first column and the new created one
    return reduced_df.iloc[:, [0]].join(reduced_df[keywords])


if __name__ == "__main__":
    data_dir = "/Users/yanzhe.li/Documents/finance/sec_clean/data"
    target_dir = "test"
    csv_dir = os.path.join(data_dir, target_dir)
    keywords = config.Intangible_keywords
    csv_runner(csv_dir, keywords)
