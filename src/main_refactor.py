import pandas as pd
import polars as pl
import secret_finder
import file_preprocessor
import export_dataframe
import os
import sys
from io import StringIO
from edgar import *

# from .. import config
pwd = os.getcwd()
root_directory = os.path.abspath(os.path.join(pwd, ".."))
sys.path.append(root_directory)
import config

keywords = config.Intangible_keywords


def process_attachments(results_df, year, stored_attachments, filing_10k_by_year):
    for i, filing in enumerate(filing_10k_by_year[year]):
        new_row = process_filing(filing, stored_attachments, i)
        if len(new_row) > 0:
            results_df = pd.concat(
                [results_df, pd.DataFrame([new_row])], ignore_index=True
            )
    return results_df


def process_filing(filing, stored_attachments, filling_index):
    filing_date = filing.filing_date
    cik = filing.cik
    company_name = filing.company
    indicator = 0
    url = None
    accession_no = filing.accession_no
    if filing.attachments:
        return process_attachment(
            filing,
            stored_attachments,
            indicator,
            url,
            accession_no,
            company_name,
            filing_date,
            cik,
        )


def process_attachment(
    filing,
    stored_attachments,
    indicator,
    url,
    accession_no,
    company_name,
    filing_date,
    cik,
):
    list_df = None
    try:
        first_attachment_url = filing.attachments[0].url
        content = stored_attachments.get(first_attachment_url)
        url = first_attachment_url
        s = StringIO(content)
        list_df = pd.read_html(s)
        if secret_finder.contains_trade_secret(keywords, content):
            indicator = 1
    except Exception as e:
        print(
            f"Error happened while calling read_html() for {filing_date}, {company_name}: {str(e)}"
        )
        list_df = []

    return process_list_df(
        list_df,
        indicator,
        url,
        accession_no,
        company_name,
        filing_date,
        cik,
    )


def process_list_df(
    list_df,
    indicator,
    url,
    accession_no,
    company_name,
    filing_date,
    cik,
):
    intangible_asset_form = pd.DataFrame()
    intangible_table_cnt = 0
    for form_df in list_df:
        texts = form_df.to_markdown()
        find_match = secret_finder.find_secret(keywords, texts)

        if find_match:
            intangible_table_cnt += 1
            intangible_asset_form = form_df
            export_dataframe.output_to_csv(
                form_df,
                data_path=os.path.join(root_directory, "data"),
                folder="intangible",
                filename=f"{filing_date}_{cik}_{intangible_table_cnt}.csv",
            )

    if not intangible_asset_form.empty:
        return process_target_form(
            intangible_asset_form,
            indicator,
            url,
            accession_no,
            company_name,
            filing_date,
            cik,
        )
    return export_dataframe.create_new_row(
        indicator, url, accession_no, company_name, filing_date, cik, None
    )


def process_target_form(
    target_trade_secret_form,
    indicator,
    url,
    accession_no,
    company_name,
    filing_date,
    cik,
):
    target_trade_secret_form = pl.from_pandas(target_trade_secret_form)
    trade_secrets: float = None
    for form_row in target_trade_secret_form.rows():
        if form_row[0]:
            if secret_finder.find_secret(keywords, str(form_row[0]).lower()):
                for item in form_row:
                    try:
                        if float(item) > 0:
                            try:
                                trade_secrets = float(item)
                            except ValueError:
                                print(f"Edge case: {filing_date} {cik} {company_name}")
                                break
                            break
                        print(form_row[0])
                        print("Unexpected case")
                    except ValueError:
                        continue
                    except TypeError:
                        continue
    return export_dataframe.create_new_row(
        indicator, url, accession_no, company_name, filing_date, cik, trade_secrets
    )


def sec_helper(start_year, end_year, file_name, filing_10k_by_year, redownload=False):
    results_df = pd.DataFrame(columns=config.COLUMN_NAMES)
    if redownload:
        file_preprocessor.download_files(
            start_year, end_year, filing_10k_by_year, file_name
        )

    for year in range(start_year, end_year + 1):
        stored_attachments = file_preprocessor.load_attachments(file_name, year)
        results_df = process_attachments(
            results_df, year, stored_attachments, filing_10k_by_year
        )
    return results_df


if __name__ == "__main__":
    set_identity("jason.xu071498@gmail.com")
    start_year, end_year = config.START_YEAR, config.END_YEAR
    filename = config.FILE_NAME

    filling_10k_by_year = file_preprocessor.filter_filling_by_year(
        start_year, end_year, slice=50
    )

    df = sec_helper(start_year, end_year, filename, filling_10k_by_year)
    # export_dataframe.output_to_csv(df, f"{filename}:{start_year}-{end_year}.csv")
