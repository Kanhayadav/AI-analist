import pandas as pd


def find_column(column_mapping, target):

    """
    Finds the actual dataframe column
    mapped to a business concept.
    """

    for column, semantic in column_mapping.items():

        if semantic == target:
            return column

    return None


def business_features(df, column_mapping):

    report = {}

    revenue_col = find_column(column_mapping, "Revenue")
    cost_col = find_column(column_mapping, "Cost")
    profit_col = find_column(column_mapping, "Profit")
    quantity_col = find_column(column_mapping, "Quantity")
    price_col = find_column(column_mapping, "Price")

    # ------------------------------------
    # Revenue = Quantity × Price
    # ------------------------------------
    if (
        revenue_col is None
        and quantity_col is not None
        and price_col is not None
    ):

        df["Revenue"] = (
            df[quantity_col] * df[price_col]
        )

        revenue_col = "Revenue"

        report["Revenue"] = {
            "generated": True,
            "formula": f"{quantity_col} * {price_col}"
        }

    # ------------------------------------
    # Profit = Revenue - Cost
    # ------------------------------------
    if (
        profit_col is None and revenue_col is not None and cost_col is not None):

        df["Profit"] = (
            df[revenue_col] - df[cost_col]
        )

        report["Profit"] = {
            "generated": True,
            "formula": f"{revenue_col} - {cost_col}"
        }

    if (
        "Profit" in df.columns
        and revenue_col is not None
    ):

        df["Profit Margin"] = (
            df["Profit"] / df[revenue_col]
        ).replace([float("inf"), float("-inf")], 0)

        df["Profit Margin"] = (
            df["Profit Margin"]
            .fillna(0)
            .round(4)
        )

        report["Profit Margin"] = {
            "generated": True,
            "formula": "Profit / Revenue"
        }

    return df, report