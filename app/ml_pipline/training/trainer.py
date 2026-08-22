from .regression import train_regression


def train_model(

    X_train,
    X_test,
    y_train,
    y_test,
    query_report

):

    task = query_report["task"]

    if task == "Regression":

        return train_regression(

            X_train,
            X_test,
            y_train,
            y_test

        )

    elif task == "Time Series Forecasting":

        # Temporary
        return train_regression(

            X_train,
            X_test,
            y_train,
            y_test

        )

    else:

        raise ValueError(
            f"{task} not supported yet."
        )   