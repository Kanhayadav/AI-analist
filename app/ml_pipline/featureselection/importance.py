from sklearn.ensemble import RandomForestRegressor


def feature_importance(X, y):

    numeric = X.select_dtypes(include="number")

    model = RandomForestRegressor(
        random_state=42
    )

    model.fit(numeric, y)

    report = dict(
        zip(
            numeric.columns,
            model.feature_importances_
        )
    )

    report = dict(
        sorted(
            report.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    return report