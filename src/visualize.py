import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_monthly_sales(df: pd.DataFrame, output_dir: str) -> None:
    monthly_sales = (
        df.groupby("order_month", as_index=False)["sales"]
        .sum()
        .sort_values("order_month")
    )

    plt.figure(figsize=(10, 5))
    plt.plot(monthly_sales["order_month"], monthly_sales["sales"], marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "monthly_sales_trend.png"))
    plt.close()


def plot_monthly_profit(df: pd.DataFrame, output_dir: str) -> None:
    if "profit" not in df.columns:
        return

    monthly_profit = (
        df.groupby("order_month", as_index=False)["profit"]
        .sum()
        .sort_values("order_month")
    )

    plt.figure(figsize=(10, 5))
    plt.plot(monthly_profit["order_month"], monthly_profit["profit"], marker="o")
    plt.title("Monthly Profit Trend")
    plt.xlabel("Month")
    plt.ylabel("Profit")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "monthly_profit_trend.png"))
    plt.close()


def plot_sales_anomalies(anomalies_df: pd.DataFrame, output_dir: str) -> None:
    plt.figure(figsize=(12, 5))
    plt.plot(anomalies_df["order_day"], anomalies_df["sales"], marker="o", label="Daily Sales")

    spikes = anomalies_df[anomalies_df["anomaly_type"] == "Spike"]
    drops = anomalies_df[anomalies_df["anomaly_type"] == "Drop"]

    if not spikes.empty:
        plt.scatter(spikes["order_day"], spikes["sales"], s=80, label="Spike")

    if not drops.empty:
        plt.scatter(drops["order_day"], drops["sales"], s=80, label="Drop")

    plt.title("Sales Anomaly Detection")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "sales_anomalies.png"))
    plt.close()


def plot_sales_forecast(history_df: pd.DataFrame, forecast_df: pd.DataFrame, output_dir: str) -> None:
    daily_sales = (
        history_df.groupby("order_day", as_index=False)["sales"]
        .sum()
        .sort_values("order_day")
    )

    daily_sales["order_day"] = pd.to_datetime(daily_sales["order_day"])
    forecast_df["date"] = pd.to_datetime(forecast_df["date"])

    plt.figure(figsize=(12, 5))
    plt.plot(daily_sales["order_day"], daily_sales["sales"], label="Historical Sales")
    plt.plot(forecast_df["date"], forecast_df["forecast_sales"], label="Forecast Sales")
    plt.title("Sales Forecast")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "sales_forecast.png"))
    plt.close()

def plot_iforest_anomalies(iforest_df: pd.DataFrame, output_dir: str) -> None:
    plt.figure(figsize=(12, 5))
    plt.plot(iforest_df["order_day"], iforest_df["sales"], label="Daily Sales")

    spikes = iforest_df[iforest_df["iforest_type"] == "Spike"]
    drops = iforest_df[iforest_df["iforest_type"] == "Drop"]

    if not spikes.empty:
        plt.scatter(spikes["order_day"], spikes["sales"], s=80, label="IForest Spike")

    if not drops.empty:
        plt.scatter(drops["order_day"], drops["sales"], s=80, label="IForest Drop")

    plt.title("Isolation Forest Sales Anomalies")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "iforest_sales_anomalies.png"))
    plt.close()


def plot_timeseries_anomalies(ts_df: pd.DataFrame, output_dir: str) -> None:
    plt.figure(figsize=(12, 5))
    plt.plot(ts_df["order_day"], ts_df["sales"], label="Actual Sales")
    plt.plot(ts_df["order_day"], ts_df["expected_sales"], label="Expected Sales")

    spikes = ts_df[ts_df["ts_type"] == "Spike"]
    drops = ts_df[ts_df["ts_type"] == "Drop"]

    if not spikes.empty:
        plt.scatter(spikes["order_day"], spikes["sales"], s=80, label="TS Spike")

    if not drops.empty:
        plt.scatter(drops["order_day"], drops["sales"], s=80, label="TS Drop")

    plt.title("Time-Series Residual Anomalies")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "timeseries_sales_anomalies.png"))
    plt.close()
        