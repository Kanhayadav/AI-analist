from .encoder import encode_features
from .scaler import scale_features
from .spliter import split_dataset


def preprocess(X, y):

    report = {}

    X, encoder_report = encode_features(X)
    report["encoding"] = encoder_report

    X, scaler, scaler_report = scale_features(X)
    report["scaling"] = scaler_report

    (
        X_train,
        X_test,
        y_train,
        y_test,
        split_report
    ) = split_dataset(
        X,
        y
    )

    report["split"] = split_report

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
        report
    )