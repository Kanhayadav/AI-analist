import pandas as pd
def fill_missing_values(df):
    report={}

    for column in df.columns:
        missing_before=df[column].isna().sum()
        if(missing_before==0):
            continue

        if pd.api.types.is_numeric_dtype(df[column]):
            median=df[column].median()
            df[column]=df[column].fillna(median)
            strategy="median"
            value_used = median
        else:
            mode=df[column].mode()[0]
            df[column]=df[column].fillna(mode)
            strategy="mode"
            value_used = mode
        report[column]={
            "filled":int(missing_before),
            "strategy":strategy,
            "value_used": str(value_used)
        }
    return df,report