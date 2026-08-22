from pathlib import Path
from datetime import datetime

RAW_FOLDER = Path("data/raw")
CLEAN_FOLDER = Path("data/cleaned")

RAW_FOLDER.mkdir(parents=True, exist_ok=True)
CLEAN_FOLDER.mkdir(parents=True, exist_ok=True)


def generate_filename(filename: str):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    name = Path(filename).stem

    extension = Path(filename).suffix

    return f"{name}_{timestamp}{extension}"


def save_raw_file(contents: bytes, filename: str):

    new_name = generate_filename(filename)

    path = RAW_FOLDER / new_name

    with open(path, "wb") as f:
        f.write(contents)

    return path


def save_clean_dataframe(df, raw_path):

    clean_name = raw_path.stem + "_clean.csv"

    clean_path = CLEAN_FOLDER / clean_name

    df.to_csv(clean_path, index=False)

    return clean_path