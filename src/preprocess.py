import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)

    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    numeric_cols = ["sales", "profit", "quantity"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["order_date", "sales"])

    if "sales" in df.columns:
        df = df[df["sales"] >= 0]

    if "profit" in df.columns:
        df["profit_margin"] = df["profit"] / df["sales"]
        df["profit_margin"] = df["profit_margin"].replace([float("inf"), -float("inf")], 0)
        df["profit_margin"] = df["profit_margin"].fillna(0)

    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["order_day"] = df["order_date"].dt.date

    return df