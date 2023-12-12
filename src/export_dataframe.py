import pandas as pd


def output_to_csv(df, filename):
    df.to_csv(filename, index=False)
