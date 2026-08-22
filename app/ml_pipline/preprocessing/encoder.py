from sklearn.preprocessing import OneHotEncoder
import pandas as pd


def encode_features(X):

    categorical = X.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    numerical = X.select_dtypes(
        exclude=["object", "category", "bool"]
    )

    if len(categorical) == 0:

        return X, {
            "encoded_columns": []
        }

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    )

    encoded = encoder.fit_transform(
        X[categorical]
    )

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(categorical),
        index=X.index
    )

    X = pd.concat(
        [
            numerical,
            encoded_df
        ],
        axis=1
    )

    report = {
        "encoded_columns": list(categorical),
        "new_feature_count": X.shape[1]
    }

    return X, report