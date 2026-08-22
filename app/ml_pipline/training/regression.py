import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from app.service.model_manager import save_model

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    root_mean_squared_error
)

def train_regression(
    X_train,
    X_test,
    y_train,
    y_test
):

    models = {

        "Linear Regression": LinearRegression(),

        "Random Forest": RandomForestRegressor(
            random_state=42,
            n_estimators=100
        )

    }

    report = {}

    best_model = None
    best_model_name = None
    best_r2 = -np.inf

    for name, model in models.items():

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        r2 = r2_score(
            y_test,
            predictions
        )

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = root_mean_squared_error(
            y_test,
            predictions
        )

        report[name] = {

            "R2": round(r2, 4),

            "MAE": round(mae, 4),

            "RMSE": round(rmse, 4)

        }

        if r2 > best_r2:

            best_r2 = r2
            best_model = model
            best_model_name = name
    model_path = save_model(
    best_model
    )

    return {

    "model": best_model,

    "best_model_name": best_model_name,

    "model_path": model_path,

    "metrics": report

    }