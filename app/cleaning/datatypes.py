import pandas as pd

def detect_dtypes(df):

    report = {}

    for column in df.columns:

        report[column] = str(df[column].dtype)

    return df, report