import pandas as pd


def datetime_features(df, column_mapping):

    report = {}

    for column, semantic in column_mapping.items():

        # Only process columns mapped as Date
        if semantic != "Date":
            continue

        try:

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            # Skip if conversion completely failed
            if converted.isna().all():
                continue

            df[column] = converted

            df[f"{column}_Year"] = converted.dt.year
            df[f"{column}_Month"] = converted.dt.month
            df[f"{column}_Quarter"] = converted.dt.quarter
            df[f"{column}_Day"] = converted.dt.day
            df[f"{column}_Weekday"] = converted.dt.day_name()
            df[f"{column}_Weekend"] = (
                converted.dt.dayofweek >= 5
            )

            report[column] = {
                "generated": [
                    f"{column}_Year",
                    f"{column}_Month",
                    f"{column}_Quarter",
                    f"{column}_Day",
                    f"{column}_Weekday",
                    f"{column}_Weekend"
                ]
            }

        except Exception as e:

            report[column] = {
                "error": str(e)
            }

    return df, report