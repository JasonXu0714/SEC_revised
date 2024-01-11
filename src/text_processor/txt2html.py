import os
from pathlib import Path
from glob import glob


def txt_to_html(txt_file_path, html_file_path):
    """
    Convert a text file to an HTML file.

    :param txt_file_path: Path to the input .txt file
    :param html_file_path: Path to the output .html file
    """
    try:
        with open(txt_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(html_file_path, "w", encoding="utf-8") as file:
            file.write("<!DOCTYPE html>\n")
            file.write("<html>\n")
            file.write("<head>\n")
            file.write("<title>" + os.path.basename(txt_file_path) + "</title>\n")
            file.write("</head>\n")
            file.write("<body>\n")

            for line in lines:
                file.write("<p>" + line.strip() + "</p>\n")

            file.write("</body>\n")
            file.write("</html>\n")
    except Exception as e:
        print(f"Error converting file {txt_file_path}: {e}")


def main():
    """
    Main function to convert all .txt files in a directory to .html files.
    """
    txt_files = glob("/Users/yanzhe.li/Documents/finance/sec_clean/data/raw_data/*.txt")

    for txt_file in txt_files:
        html_file = Path(txt_file).with_suffix(".html")
        txt_to_html(txt_file, html_file)


if __name__ == "__main__":
    main()
