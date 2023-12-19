import time
import requests
import pandas as pd
import config
import file_preprocessor
import pickle
from itertools import cycle
from edgar import *


def load_proxies(file_name="proxies.csv"):
    df = pd.read_csv(file_name, header=None)  # No header
    proxies = df[0].tolist()  # Get the first (0th) column
    return proxies


def download_attachments(filing_10k_by_year, file_name, year, proxies):
    filing_attachments = {}
    proxy_pool = cycle(proxies)

    for _, filing in enumerate(filing_10k_by_year[year]):
        if filing.attachments:
            first_attachment = filing.attachments[0]
            print(first_attachment.url)

            # Get a proxy from the pool
            proxy = next(proxy_pool)
            print("Using proxy: ", proxy)

            try:
                response = requests.get(
                    first_attachment.url, proxies={"http": proxy, "https": proxy}
                )
                filing_attachments[first_attachment.url] = response.content
                time.sleep(1)
            except:
                # Most free proxies will often get connection errors, so we catch them and move on to the next proxy
                print("Skipping. Connection error")

    with open(f"{file_name}_{year}.pkl", "wb") as file:
        pickle.dump(filing_attachments, file)


if __name__ == "__main__":
    set_identity("jason.xu071498@gmail.com")
    start_year, end_year = config.START_YEAR, config.END_YEAR
    column_names = config.COLUMN_NAMES

    filename = config.FILE_NAME
    filing_10k_by_year = file_preprocessor.filter_filling_by_year(
        start_year, end_year, slice=5
    )
    proxies = load_proxies(file_name="proxies.csv")
    download_attachments(filing_10k_by_year, filename, start_year, proxies)
