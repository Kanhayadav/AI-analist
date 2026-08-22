from .duplicates import remove_duplicates
from .missing import fill_missing_values
from .datatypes import detect_dtypes
from .outliner import remove_outliers



def clean_df(df):
    report={}
    df,duplicate_report=remove_duplicates(df)
    report["duplicates"] = duplicate_report
    df,missing_report=fill_missing_values(df)
    report["missing_values"] = missing_report
    #to do ->
    df,outliner_report=remove_outliers(df)
    report["outliers"] = outliner_report
    df,datatypes_report=detect_dtypes(df)
    report["data_types"] = datatypes_report
    
    return df,report