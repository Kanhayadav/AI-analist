def recommend_models(task):

    if task == "Regression":

        return [
            "Linear Regression",
            "Random Forest Regressor",
            "XGBoost Regressor",
            "LightGBM Regressor"
        ]

    elif task == "Classification":

        return [
            "Logistic Regression",
            "Random Forest Classifier",
            "XGBoost Classifier",
            "LightGBM Classifier"
        ]

    elif task == "Time Series Forecasting":

        return [
            "ARIMA",
            "Prophet",
            "XGBoost Time Series"
        ]

    return []