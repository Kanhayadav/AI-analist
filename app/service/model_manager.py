import joblib
from pathlib import Path


MODEL_DIR = Path("saved_models")

MODEL_DIR.mkdir(exist_ok=True)


def save_model(model, name="best_model.pkl"):

    path = MODEL_DIR / name

    joblib.dump(model, path)

    return str(path)


def load_model(name="best_model.pkl"):

    path = MODEL_DIR / name

    return joblib.load(path)