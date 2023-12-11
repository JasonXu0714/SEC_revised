import pandas as pd
import polars as pl
import config
import time
import sys
import secret_finder
import file_preprocessor
from edgar import *
from tqdm import tqdm


def sec_helper(start_year, end_year, column_names, file_name, filling_10k_by_year):
    """
    Input:
        start_year
        end_year
    """
    for i in tqdm(range(start_year, end_year + 1)):
        file_preprocessor.download_attachments(
            filling_10k_by_year, file_name, i
        )  # ONLY CALL THIS FUNCTION WHEN YOU NEED TO RE-DOWNLOAD ATTACHMENTS ???
    for year in range(start_year, end_year + 1):
        stored_attachments = file_preprocessor.load_attachments(file_name, year)
        for i, filing in enumerate(filling_10k_by_year[year]):
            filing_date = filing.filing_date
            # Note: write a script to scrape conformed_year_dict
            # conformed_year = conformed_year_dict.get(filing.accession_no)
            cik = filing.cik
            company_name = filing.company
            indicator = 0
            url = None
            accession_no = filing.accession_no

            if filing.attachments:
                list_df = []
                try:
                    first_attachment_url = filing.attachments[0].url
                    print(type(url))
                    content = stored_attachments.get(first_attachment_url)
                    list_df = pd.read_html(content)
                    url = first_attachment_url

                    if secret_finder.contains_trade_secret(content):
                        indicator = 1

                except Exception as e:
                    print(
                        f"Error happened while calling read_html() for {filing_date}, {company_name}: {str(e)}"
                    )
        return list_df


if __name__ == "__main__":
    set_identity("jason.xu071498@gmail.com")

    start_year, end_year = config.START_YEAR, config.END_YEAR
    column_names = config.COLUMN_NAMES
    filename = config.FILE_NAME
    filling_10k_by_year = file_preprocessor.filter_filling_by_year(start_year, end_year)
    df = sec_helper(start_year, end_year, column_names, filename, filling_10k_by_year)
    print(df)
