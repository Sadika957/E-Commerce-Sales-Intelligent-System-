import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def forecast_sales(df: pd.DataFrame, forecast_periods: int = 30) -> pd.DataFrame:
    daily_sales = (
        df.groupby("order_day", as_index=False)["sales"]
        .sum()
        .sort_values("order_day")
    )

    daily_sales["order_day"] = pd.to_datetime(daily_sales["order_day"])
    ts = daily_sales.set_index("order_day")["sales"].asfreq("D").fillna(0)

    model = ExponentialSmoothing(
        ts,
        trend="add",
        seasonal=None
    ).fit()

    forecast_values = model.forecast(forecast_periods)

    forecast_df = pd.DataFrame({
        "date": forecast_values.index,
        "forecast_sales": forecast_values.values
    })

    return forecast_df