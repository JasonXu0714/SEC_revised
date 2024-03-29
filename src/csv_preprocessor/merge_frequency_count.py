import pandas as pd
import sys
import os
import src.export_dataframe as export_dataframe
import config


def merge_frequency_count(
    csv_dir, data_dir, folder="frequency_merged", filename="merged.csv"
):
    all_csv_files = os.listdir(csv_dir)
    dataframes = [pd.read_csv(os.path.join(csv_dir, f)) for f in all_csv_files]
    combined = pd.concat(dataframes)
    result = combined.groupby("word")["count"].sum().reset_index()
    result = result[~result["word"].apply(lambda x: x.replace(" ", "").isnumeric())]
    result = result.sort_values("count", ascending=False)
    export_dataframe.output_to_csv(result, data_dir, folder=folder, filename=filename)


if __name__ == "__main__":
    current_dir = os.getcwd()
    root_directory = config.root_directory
    data_dir = os.path.join(root_directory, "data")
    target_dir = "test_merge"
    if len(sys.argv) > 1 and sys.argv[1] == "frequency_count":
        target_dir = sys.argv[1]
    csv_dir = os.path.join(data_dir, target_dir)
    merge_frequency_count(csv_dir, data_dir)
