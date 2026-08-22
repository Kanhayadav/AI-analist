import pandas as pd

def remove_outliers(df):

    report = {}

    numeric_columns = df.select_dtypes(include=["number"]).columns

    for column in numeric_columns:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        before = len(df)

        df = df[
            (df[column] >= lower) &
            (df[column] <= upper)
        ]

        removed = before - len(df)

        report[column] = {
            "outliers_removed": removed
        }

    return df, report