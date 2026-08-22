def remove_high_missing(df, threshold=0.50):

    report = {
        "removed": []
    }

    columns_to_drop = []

    for column in df.columns:

        percent = df[column].isna().mean()

        if percent >= threshold:

            columns_to_drop.append(column)

            report["removed"].append({

                "column": column,
                "missing_percent": round(percent, 2)
            })

    df = df.drop(columns=columns_to_drop)

    return df, report