import pandas as pd
import polars as pl
import config
import time
import sys
import re
import secret_finder
import file_preprocessor
import export_dataframe
from io import StringIO
from edgar import *
from tqdm import tqdm

# keywords = ["secre", "know", "intellect", "confiden", "proprie"]
keywords = ["trade secre", "know", "intellect", "confiden", "proprie"]


def find_secret(keywords, text):
    matches = []
    for keyword in keywords:
        match = re.findall(
            r"[\w\s]*" + re.escape(keyword) + r"[\w\s]*",
            text,
            re.IGNORECASE,
        )
        if match:
            matches.extend(match)
    return len(matches) > 0


def sec_helper(start_year, end_year, column_names, file_name, filing_10k_by_year):
    """
    Input:
        start_year
        end_year
    """
    results_df = pd.DataFrame(columns=config.COLUMN_NAMES)
    # for i in tqdm(range(start_year, end_year + 1)):
    #     time.sleep(1)
    #     file_preprocessor.download_attachments(
    #         filing_10k_by_year, file_name, i
    #     )  # ONLY CALL THIS FUNCTION WHEN YOU NEED TO RE-DOWNLOAD ATTACHMENTS ???
    """
    input: filing
    output: dataframe containing secrets 
    """
    for year in range(start_year, end_year + 1):
        stored_attachments = file_preprocessor.load_attachments(file_name, year)
        for i, filing in enumerate(filing_10k_by_year[year]):
            # if i != 39 and i != 43:
            #     continue
            print(i)
            filing_date = filing.filing_date
            cik = filing.cik
            company_name = filing.company
            indicator = 0
            url = None
            accession_no = filing.accession_no

            if filing.attachments:
                list_df = None
                try:
                    first_attachment_url = filing.attachments[0].url
                    content = stored_attachments.get(first_attachment_url)
                    url = first_attachment_url
                    s = StringIO(content)
                    list_df = pd.read_html(s)

                    if secret_finder.contains_trade_secret(
                        content
                    ):  # Assuming this function checks for the presence of the keywords
                        indicator = 1

                except Exception as e:
                    print(
                        f"Error happened while calling read_html() for {filing_date}, {company_name}: {str(e)}"
                    )
                    list_df = []
                target_trade_secret_form = None
                for form_df in list_df:
                    texts = form_df.to_markdown()
                    match = find_secret(keywords, texts)
                    if match:
                        target_trade_secret_form = form_df
                        break  # no early break
                if target_trade_secret_form is not None:
                    target_trade_secret_form = pl.from_pandas(target_trade_secret_form)
                    trade_secrets: float = None

                    for form_row in target_trade_secret_form.rows():
                        if form_row[0]:
                            if find_secret(keywords, str(form_row[0]).lower()):
                                for item in form_row:
                                    try:
                                        if float(item) > 0:
                                            try:
                                                trade_secrets = float(item)
                                            except ValueError:
                                                print(
                                                    f"Edge case: {filing_date} {cik} {company_name}"
                                                )  # debug only
                                                break
                                            break
                                        print(form_row[0])
                                        print("Unexpected case")  # debug only
                                    except ValueError:
                                        continue
                                    except TypeError:
                                        continue
                    new_row = {
                        "company_name": company_name,
                        "filing_date": filing_date,
                        "cik": cik,
                        "trade_secrets": trade_secrets,
                        "indicator": indicator,
                        "url": url,
                        "accession_no": accession_no,
                    }
                    results_df = pd.concat(
                        [results_df, pd.DataFrame([new_row])], ignore_index=True
                    )
                else:
                    new_row = {
                        "company_name": company_name,
                        "filing_date": filing_date,
                        "cik": cik,
                        "trade_secrets": None,
                        "indicator": indicator,
                        "url": url,
                        "accession_no": accession_no,
                    }
                    results_df = pd.concat(
                        [results_df, pd.DataFrame([new_row])], ignore_index=True
                    )
                    print(f"No DataFrame contains specified keywords in filing {i}.")
        return results_df


if __name__ == "__main__":
    set_identity("jason.xu071498@gmail.com")
    start_year, end_year = config.START_YEAR, config.END_YEAR
    column_names = config.COLUMN_NAMES

    filename = config.FILE_NAME
    filling_10k_by_year = file_preprocessor.filter_filling_by_year(
        start_year, end_year, slice=50
    )

    df = sec_helper(start_year, end_year, column_names, filename, filling_10k_by_year)
    export_dataframe.output_to_csv(df, f"{filename}:{start_year}-{end_year}.csv")
