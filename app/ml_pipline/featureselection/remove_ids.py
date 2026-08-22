import pandas as pd


ID_KEYWORDS = [
    "id",
    "code",
    "number",
    "no",
    "Order ID",
    "uuid"
]


def remove_ids(df):

    report = {
        "removed": []
    }

    columns_to_drop = []

    for column in df.columns:

        name = column.lower()

        if any(keyword in name for keyword in ID_KEYWORDS):

            columns_to_drop.append(column)
            report["removed"].append(column)

    df = df.drop(columns=columns_to_drop)

    return df, report