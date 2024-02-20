import os
from pathlib import Path
from glob import glob
from multiprocessing import Pool
from tqdm import tqdm


# read_str(file_path, encoding="latin1"):


# Reads the content of a file specified by file_path.
# Returns the content as a list of lines.
# Uses "latin1" encoding by default, which can be changed based on file encoding.
def read_str(file_path, encoding="latin1"):
    """
    Reads the contents of a file and returns it as a list of lines.
    """
    # with open(file_path, encoding=encoding) as file:: This line uses the with statement to open a file.
    with open(file_path, encoding=encoding) as file:
        return file.read().splitlines()


# process(file_path):
def is_annual_report(file_path):
    """sampel input /...../filename.txt"""
    if not os.path.isfile(file_path):
        return False

    # Get the file name from the file path
    file_name = os.path.basename(file_path)
    file_name = file_path.split("/")[-1]
    filing_type = file_name.split("_")[1]
    return "K" in filing_type


# Takes a file path, reads its content, and looks for specific HTML tags (</html>, </document>, </xbrl>).
# Stops reading the file once one of these tags is found.
# Saves the read content to a new file in a directory named first_html.
# The directory structure of the output files mirrors that of the input files, with the only difference being the base directory name (filings replaced by first_html).
# The commented-out line
# converted_text = html2text("\n".join(html_content)) suggests an intention to convert HTML to plain text,
# but it's currently not active, and instead, the HTML content is saved as is. ???
def process(file_path, output_folder="first_html"):
    """
    Processes each file to extract HTML content and convert it to text.
    Saves the converted text in a specified directory.
    """
    # won't process 10q file
    if not is_annual_report(file_path):
        return
    output_path = Path(file_path.replace("raw_data", output_folder))
    output_path.parent.mkdir(exist_ok=True, parents=True)

    html_content = []
    html_found = False
    for line in read_str(file_path):
        html_content.append(line)
        if any(tag in line.lower() for tag in ["</html>", "</document>", "</xbrl>"]):
            html_found = True
            break
    if not html_found:
        print(f"No HTML code found in file {file_path}. Skipping processing.")
        return
    try:
        #         converted_text = html2text("\n".join(html_content))
        converted_text = "\n".join(html_content)
        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write(converted_text)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def main():
    """
    Main function to process files in parallel using multiprocessing.
    """
    # don't forget to replace file path with your original data path(txt file)
    root_dir = os.getcwd()
    input_path = os.path.join(root_dir, "data/raw_data/**")
    file_paths = glob(input_path, recursive=True)
    with Pool(20) as pool:
        with tqdm(total=len(file_paths)) as progress_bar:
            for _ in pool.imap(process, file_paths):
                progress_bar.update(1)


# main():

# This is the entry point of the script when run as a main program.
# It finds all file paths matching the pattern filings/*/*/*/* using glob.
# It uses a multiprocessing pool (Pool(20)) to process these files in parallel,
# which can significantly speed up the process on multi-core systems.
# The progress of processing is displayed using tqdm, which shows a progress bar.
if __name__ == "__main__":
    main()
