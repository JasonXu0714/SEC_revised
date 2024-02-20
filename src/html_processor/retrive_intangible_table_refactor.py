import pandas as pd
import src.secret_finder as secret_finder
import src.export_dataframe as export_dataframe
import os
import sys
from glob import glob
import config
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool
from src.time.timer import Timer
from src.utils.dir_utils import create_dir_structure

keywords = config.Intangible_keywords


def html_runner(html_dir, output_folder):
    """
    Input:
        html_dir:directory to store raw html file
        output_folder:csv file transformed from html file with key words
        max_file: num of files to process each time
    """

    all_html_files = os.listdir(html_dir)
    p = Pool()
    with tqdm(total=len(all_html_files)) as progress_bar:
        for _ in p.starmap(
            read_html_file,
            [(html_dir, output_folder, filename) for filename in all_html_files],
        ):
            progress_bar.update(1)


def process_file(file_path, src_dir, output_dir):
    if not os.path.isfile(file_path):
        return
    file_name = Path(file_path).name
    file_dir = Path(file_path).parent
    new_dir = create_dir_structure(file_path, src_dir, output_dir)
    print(file_path)
    print("\n")
    # Ensure the new_dir does not include the file name
    read_html_file(src_dir=file_dir, output_folder=new_dir, filename=file_name)


def read_html_file(src_dir, output_folder, filename):
    print(src_dir)
    print("\n")
    try:
        with open(os.path.join(src_dir, filename), "r") as f:
            list_df = pd.read_html(f)
    except ValueError as e:
        # print(e)
        return
    process_list_df(list_df, output_folder, filename)


def process_list_df(
    list_df,
    output_folder,
    file_name,
):
    form_number = 0
    for form_df in list_df:
        texts = form_df.to_markdown()
        find_match = secret_finder.find_secret(keywords, texts)
        if find_match:
            file_name_without_extension = file_name.split(".")[0]
            file_name_with_index = file_name_without_extension + f"_{form_number}.csv"
            output_dir = Path(output_folder)
            export_dataframe.output_to_csv(
                form_df,
                folder=output_dir,
                filename=file_name_with_index,
            )
            form_number += 1


def main(src_dir, output_dir):
    file_paths = glob(os.path.join(src_dir, "**"), recursive=True)
    timer = Timer()
    timer.start()
    with Pool(20) as pool:
        tasks = []
        for file_path in tqdm(file_paths):
            task = pool.apply_async(process_file, args=(file_path, src_dir, output_dir))
            tasks.append(task)
        pool.close()
        for task in tasks:
            task.get()  # Wait for the task to complete
        pool.join()
    timer.stop()
    print(f"Elapsed time: {timer.elapsed_time()} seconds")


if __name__ == "__main__":
    data_dir = Path.cwd() / "data"
    src_folder, dest_folder = sys.argv[1:]
    src_dir = Path.joinpath(data_dir, src_folder)
    dest_dir = Path.joinpath(data_dir, dest_folder)
    main(src_dir, dest_dir)
