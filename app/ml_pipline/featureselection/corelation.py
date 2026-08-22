import numpy as np


def remove_correlated_features(X, threshold=0.90):

    numeric = X.select_dtypes(include="number")

    corr = numeric.corr().abs()

    upper = corr.where(
        np.triu(np.ones(corr.shape), k=1).astype(bool)
    )

    drop_columns = [
        column
        for column in upper.columns
        if any(upper[column] > threshold)
    ]

    X = X.drop(columns=drop_columns)

    report = {
        "removed": drop_columns
    }

    return X, report