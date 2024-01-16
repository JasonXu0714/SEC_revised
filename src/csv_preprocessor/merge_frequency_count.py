import pandas as pd
import sys
import os
import src.export_dataframe as export_dataframe
import config


def is_not_numeric(x):
    try:
        return not x.replace(" ", "").isnumeric()
    except AttributeError:
        print(x)
        return True


def merge_frequency_count(csv_dir, folder, filename="merged.csv"):
    all_csv_files = os.listdir(csv_dir)
    dataframes = [pd.read_csv(os.path.join(csv_dir, f)) for f in all_csv_files]
    combined = pd.concat(dataframes)
    result = combined.groupby("word")["count"].sum().reset_index()
    result = result[result["word"].apply(is_not_numeric)]
    result = result.sort_values("count", ascending=False)
    export_dataframe.output_to_csv(result, folder=folder, filename=filename)


if __name__ == "__main__":
    root_directory = config.root_directory
    data_dir = os.path.join(root_directory, "data")
    src_dir, dest_dir = sys.argv[1:]
    csv_dir = os.path.join(data_dir, src_dir)
    merge_frequency_count(csv_dir, folder=dest_dir)
