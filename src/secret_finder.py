import re


def contains_trade_secret_column(df):
    # List of column names to search for
    search_columns = [
        "trade secret",
        "trade secrets",
        "net trade secret",
        "net trade secrets",
        "trade secrets (not subject to amortization)",
        "trade secrecy",
        "net trade secrecy",
    ]

    # Filter rows where the first column is a string, then check if any value matches the search_columns list
    filtered_df = df[df.iloc[:, 0].apply(lambda x: isinstance(x, str))]  # ?
    result = None
    try:
        result = any(filtered_df.iloc[:, 0].str.lower().isin(search_columns))
    except:
        return None
    return result


def contains_trade_secret(keywords, content):
    return any(keyword in content.lower() for keyword in keywords)


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
