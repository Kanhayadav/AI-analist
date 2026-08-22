from sklearn.model_selection import train_test_split


def split_dataset(X, y):

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    report = {
        "train_samples": len(X_train),
        "test_samples": len(X_test)
    }

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        report
    )