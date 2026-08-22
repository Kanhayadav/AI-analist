import pandas as pd

def remove_duplicates(df):
    before=len(df)
    df=df.drop_duplicates()
    after=len(df)

    report={
        "duplicates_removed": before-after
    }

    return df,report