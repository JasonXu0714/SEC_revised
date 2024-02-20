from pathlib import Path
import os
from glob import glob
from multiprocessing import Pool
from tqdm import tqdm


def read_str(file_path, encoding="latin1"):
    with open(file_path, encoding=encoding) as file:
        return file.read().splitlines()


def is_annual_report(file_path):
    if not os.path.isfile(file_path):
        return False
    file_name = file_path.split("/")[-1]
    filing_type = file_name.split("_")[1]
    return "K" in filing_type


def create_dir_structure(file_path, root_dir, output_dir):
    relative_path = os.path.relpath(file_path, root_dir)
    new_dir = os.path.join(output_dir, os.path.dirname(relative_path))
    os.makedirs(new_dir, exist_ok=True)
    return new_dir


def convert_txt_to_html(file_path, new_dir):
    output_path = Path(new_dir) / Path(file_path).name.replace(".txt", ".html")
    html_content = read_str(file_path)
    if not html_content:
        print(f"No HTML code found in file {file_path}. Skipping processing.")
        return

    try:
        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write("\n".join(html_content))
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def process_file(file_path, root_dir, output_dir):
    if not is_annual_report(file_path):
        return
    new_dir = create_dir_structure(file_path, root_dir, output_dir)
    convert_txt_to_html(file_path, new_dir)


def main(root_dir, output_dir):
    file_paths = glob(os.path.join(root_dir, "**"), recursive=True)
    with Pool(20) as pool:
        tasks = []
        for file_path in tqdm(file_paths):
            task = pool.apply_async(
                process_file, args=(file_path, root_dir, output_dir)
            )
            tasks.append(task)
        pool.close()
        for task in tasks:
            task.get()  # Wait for the task to complete
        pool.join()


if __name__ == "__main__":
    root_dir = Path.cwd() / "data" / "raw_data"
    output_dir = Path.cwd() / "data" / "first_html"
    main(root_dir, output_dir)
