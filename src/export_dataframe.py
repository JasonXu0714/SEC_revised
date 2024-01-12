import pandas as pd
import config
import os

data_path = config.data_directory


def create_new_row(
    indicator, url, accession_no, company_name, filing_date, cik, trade_secrets
):
    new_row = {
        "company_name": company_name,
        "filing_date": filing_date,
        "cik": cik,
        "trade_secrets": trade_secrets,
        "indicator": indicator,
        "url": url,
        "accession_no": accession_no,
    }
    return new_row


def output_to_csv(df, folder, filename, data_dir=data_path):
    file_path = os.path.join(data_dir, folder, filename)
    df.to_csv(file_path, index=False)
