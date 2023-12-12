import pandas as pd
import polars as pl
import config
import time
import sys
import secret_finder
import file_preprocessor
import export_dataframe
from edgar import *
from tqdm import tqdm


def sec_helper(start_year, end_year, column_names, file_name, filing_10k_by_year):
    """
    Input:
        start_year
        end_year
    """
    results_df = pd.DataFrame(columns=config.COLUMN_NAMES)
    for i in tqdm(range(start_year, end_year + 1)):
        time.sleep(1)
        file_preprocessor.download_attachments(
            filing_10k_by_year, file_name, i
        )  # ONLY CALL THIS FUNCTION WHEN YOU NEED TO RE-DOWNLOAD ATTACHMENTS ???
    for year in range(start_year, end_year + 1):
        stored_attachments = file_preprocessor.load_attachments(file_name, year)
        for i, filing in enumerate(filing_10k_by_year[year]):
            filing_date = filing.filing_date
            # Note: write a script to scrape conformed_year_dict
            # conformed_year = conformed_year_dict.get(filing.accession_no)
            cik = filing.cik
            company_name = filing.company
            indicator = 0
            url = None
            accession_no = filing.accession_no

            if filing.attachments:
                list_df = None
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
                    list_df = []

                # Variable to store the DataFrame if found
                target_trade_secret_form = None

                # Iterate over each DataFrame in the list
                for form_df in list_df:
                    # Check if the string 'trade secret' is present in the DataFrame (case-insensitive)
                    if "trade secret" in form_df.to_markdown().lower():
                        # if contains_trade_secret_column(form_df):
                        # If found, assign this DataFrame to variable 'a' and break the loop
                        target_trade_secret_form = form_df
                        break

                # Check if a DataFrame containing 'trade secret' was found
                if target_trade_secret_form is not None:
                    # Convert the pandas DataFrame 'target_k10_form' to a Polars DataFrame for further processing
                    target_trade_secret_form = pl.from_pandas(target_trade_secret_form)
                    trade_secrets: float = None
                    net_trade_secrets: float = None
                    # Iterate over each row in the Polars DataFrame
                    for form_row in target_trade_secret_form.rows():
                        # Check if the first element of the row is not null or empty
                        if form_row[0]:
                            # Check if the string 'secret' is present in the first element (case-insensitive)
                            if "secret" in form_row[0]:
                                # Iterate over each element in the current row
                                for item in form_row:
                                    try:
                                        # Attempt to convert the element to a float and check if it's greater than 0
                                        if float(item) > 0:
                                            if (
                                                form_row[0].lower()
                                                == "net trade secret"
                                                or form_row[0].lower()
                                                == "net trade secrets"
                                                or form_row[0].lower()
                                                == "net trade secrecy"
                                            ):
                                                net_trade_secrets = float(item)
                                                break
                                            # elif form_row[0].lower() == "trade secret" or form_row[0].lower() == "trade secrets" or form_row[0].lower() == "trade secrets (not subject to amortization)":
                                            elif (
                                                "trade secret" in form_row[0].lower()
                                                or "trade secrecy"
                                                in form_row[0].lower()
                                            ):
                                                try:
                                                    trade_secrets = float(item)
                                                except Exception as e:
                                                    print(
                                                        f"Edge case: {filing_date} {cik} {company_name}"
                                                    )  # debug only
                                                    break
                                                break
                                            else:
                                                print(form_row[0])
                                                print("Unexpected case")  # debug only
                                    except ValueError:
                                        # If an error occurs (e.g., when the element cannot be converted to a float), continue to the next element
                                        continue
                                    except TypeError:
                                        continue

                    new_row = pd.DataFrame(
                        [
                            {
                                "company_name": company_name,
                                "filing_date": filing_date,
                                "cik": cik,
                                "trade_secrets": trade_secrets,
                                "net_trade_secrets": net_trade_secrets,
                                "indicator": indicator,
                                "url": url,
                                "accession_no": accession_no,
                            }
                        ]
                    )
                    # Concatenate the new row to the results DataFrame
                    results_df = pd.concat([results_df, new_row], ignore_index=True)
                else:
                    new_row = pd.DataFrame(
                        [
                            {
                                "company_name": company_name,
                                "filing_date": filing_date,
                                "cik": cik,
                                "trade_secrets": None,
                                "net_trade_secrets": None,
                                "indicator": indicator,
                                "url": url,
                                "accession_no": accession_no,
                            }
                        ]
                    )
                    # Concatenate the new row to the results DataFrame
                    results_df = pd.concat([results_df, new_row], ignore_index=True)
                    print(f"No DataFrame contains 'trade secret' in filing {i}.")
    return results_df


if __name__ == "__main__":
    set_identity("jason.xu071498@gmail.com")
    start_year, end_year = config.START_YEAR, config.END_YEAR
    column_names = config.COLUMN_NAMES

    filename = config.FILE_NAME
    filling_10k_by_year = file_preprocessor.filter_filling_by_year(
        start_year, end_year, slice=5
    )

    df = sec_helper(start_year, end_year, column_names, filename, filling_10k_by_year)
    export_dataframe.output_to_csv(df, f"{filename}:{start_year}-{end_year}.csv")
