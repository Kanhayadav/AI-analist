from .remove_ids import remove_ids
from .remove_constants import remove_constant
from .remove_high_missing_values import remove_high_missing
from .targetselector import select_target
from .corelation import remove_correlated_features
from .mutual_info import mutual_information
from .importance import feature_importance


def feature_selector(df, query_report):

    report = {}

    df, id_report = remove_ids(df)
    report["id_columns"] = id_report

    df, constant_report = remove_constant(df)
    report["constant_columns"] = constant_report

    df, missing_report = remove_high_missing(df)
    report["high_missing_columns"] = missing_report

    X, y, target_report = select_target(
        df,
        query_report
    )

    report["target"] = target_report

    # ---------------------------------------
    # Remove raw datetime columns
    # ---------------------------------------
    datetime_columns = X.select_dtypes(
        include=["datetime", "datetimetz"]
    ).columns.tolist()

    if datetime_columns:

        X = X.drop(columns=datetime_columns)

        report["datetime_columns"] = {
            "removed": datetime_columns
        }

    # ---------------------------------------
    # Correlation
    # ---------------------------------------
    X, corr_report = remove_correlated_features(X)

    report["correlation"] = corr_report

    # ---------------------------------------
    # Mutual Information
    # ---------------------------------------
    report["mutual_information"] = mutual_information(
        X,
        y
    )

    # ---------------------------------------
    # Feature Importance
    # ---------------------------------------
    report["feature_importance"] = feature_importance(
        X,
        y
    )

    return X, y, report