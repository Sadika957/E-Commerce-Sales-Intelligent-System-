import pandas as pd


def generate_kpis(df: pd.DataFrame) -> dict:
    total_sales = float(df["sales"].sum())
    total_profit = float(df["profit"].sum()) if "profit" in df.columns else 0.0
    total_orders = int(df["order_id"].nunique()) if "order_id" in df.columns else int(len(df))
    average_order_value = float(total_sales / total_orders) if total_orders > 0 else 0.0

    return {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "total_orders": total_orders,
        "average_order_value": round(average_order_value, 2)
    }


def monthly_sales_summary(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby("order_month", as_index=False)["sales"]
        .sum()
        .sort_values("order_month")
    )
    return monthly


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if "product_name" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("product_name", as_index=False)[["sales", "profit"]]
        .sum()
        .sort_values("sales", ascending=False)
        .head(n)
    )


def top_categories(df: pd.DataFrame) -> pd.DataFrame:
    if "category" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("category", as_index=False)[["sales", "profit"]]
        .sum()
        .sort_values("sales", ascending=False)
    )