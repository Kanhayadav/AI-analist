def remove_constant(df):

    report = {
        "removed": []
    }

    columns_to_drop = []

    for column in df.columns:

        if df[column].nunique() <= 1:

            columns_to_drop.append(column)
            report["removed"].append(column)

    df = df.drop(columns=columns_to_drop)

    return df, report