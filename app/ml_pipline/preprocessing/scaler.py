from sklearn.preprocessing import StandardScaler


def scale_features(X):

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    report = {
        "scaled_features": X.shape[1]
    }

    return X_scaled, scaler, report