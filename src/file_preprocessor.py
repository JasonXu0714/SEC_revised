import pickle
import time
from tqdm import tqdm
from edgar import *


def download_attachments(filing_10k_by_year, file_name, year):
    # Initialize an empty dictionary to store attachments.
    filing_attachments = {}
    # key: attachment URL, value: file object of the html attachment

    # Loop through each filing in the provided list of 10-K filings.
    for _, filing in enumerate(filing_10k_by_year[year]):
        # Check if the current filing has any attachments.
        if filing.attachments:
            # Select the first attachment of the current filing.
            first_attachment = filing.attachments[0]
            print(first_attachment.url)
            # Download the attachment and store it in the dictionary with its URL as the key.
            filing_attachments[first_attachment.url] = first_attachment.download()
            time.sleep(1)

    # Open a file with the given file name in write-binary mode.
    with open(f"{file_name}_{year}.pkl", "wb") as file:
        # Serialize and save the dictionary of attachments to the file.
        pickle.dump(filing_attachments, file)


def load_attachments(file_name, year):
    # Open the specified file in read-binary mode.
    with open(f"data/attchment/{file_name}_{year}.pkl", "rb") as file:
        loaded_data = pickle.load(file)
        return loaded_data


def filter_filling_by_year(start_year, end_year, slice=5):
    """
    Fetch filings for the specified year range
    Input:
        year range
    Output:
        10k form for targeted year range
    """
    filing_10k_by_year = {}
    for year in range(start_year, end_year + 1):
        time.sleep(0.5)
        filing_10k = (
            get_filings(year=year).filter(form=["10-K"]).latest(slice)
        )  # must greater than one otherwise not iterable
        filing_10k_by_year[year] = filing_10k  # ?
    return filing_10k_by_year


def download_files(start_year, end_year, filing_10k_by_year, file_name):
    for i in tqdm(range(start_year, end_year + 1)):
        time.sleep(1)
        download_attachments(filing_10k_by_year, file_name, i)
