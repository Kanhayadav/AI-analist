import pandas as pd


def detect_task(df, column_mapping):

    report = {}

    regression_targets = []
    classification_targets = []
    datetime_columns = []

    # Find datetime columns
    for column in df.columns:

        if pd.api.types.is_datetime64_any_dtype(df[column]):
            datetime_columns.append(column)

    # Analyze every column
    for column in df.columns:

        # Skip datetime columns
        if column in datetime_columns:
            continue

        unique_values = df[column].nunique()

        # Numeric columns
        if pd.api.types.is_numeric_dtype(df[column]):

            # Continuous values
            if unique_values > 20:
                regression_targets.append(column)

            # Few unique values -> Classification
            else:
                classification_targets.append(column)

        # Object / String columns
        else:

            if unique_values <= 20:
                classification_targets.append(column)

    if datetime_columns and regression_targets:

        task = "Time Series Forecasting"

    elif regression_targets:

        task = "Regression"

    elif classification_targets:

        task = "Classification"

    else:

        task = "Unknown"

    report = {

        "recommended_task": task,

        "candidate_targets": {

            "regression": regression_targets,

            "classification": classification_targets

        },

        "datetime_columns": datetime_columns

    }

    return report