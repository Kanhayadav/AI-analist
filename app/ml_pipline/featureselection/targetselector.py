def select_target(df, query_report):

    target = query_report.get("target")

    if target is None:
        raise ValueError("No target identified from user query.")

    if target not in df.columns:
        raise ValueError(f"{target} not found in dataset.")

    X = df.drop(columns=[target])
    y = df[target]

    report = {
        "target": target,
        "task": query_report.get("task"),
        "forecast_horizon": query_report.get("forecast_horizon"),
        "feature_count": X.shape[1],
        "sample_count": X.shape[0]
    }

    return X, y, report