import joblib
import pandas as pd


def predict(model, X):

    predictions = model.predict(X)

    return predictions.tolist()