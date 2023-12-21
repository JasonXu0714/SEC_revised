import pandas as pd
import os


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


def output_to_csv(df, filename):
    pwd = os.getcwd()
    file_path = f"{pwd}/../data/{filename}"
    df.to_csv(file_path, index=False)
