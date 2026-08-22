from sklearn.feature_selection import mutual_info_regression
import pandas as pd


def mutual_information(X, y):

    numeric = X.select_dtypes(include="number")

    scores = mutual_info_regression(
        numeric,
        y
    )

    report = dict(
        zip(
            numeric.columns,
            scores
        )
    )

    report = dict(
        sorted(
            report.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    return report