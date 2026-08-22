from .business_features import business_features
from .datetime_features import datetime_features


def engineer_features(df, column_mapping):

    report = {}

    df, business_report = business_features(
        df,
        column_mapping
    )

    report["business_features"] = business_report

    df, datetime_report = datetime_features(
        df,
        column_mapping
    )

    report["datetime_features"] = datetime_report

    return df, report