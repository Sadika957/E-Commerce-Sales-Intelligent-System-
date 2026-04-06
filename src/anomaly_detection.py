import pandas as pd
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def prepare_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    daily_sales = (
        df.groupby("order_day", as_index=False)["sales"]
        .sum()
        .sort_values("order_day")
    )

    daily_sales["order_day"] = pd.to_datetime(daily_sales["order_day"])
    return daily_sales


def detect_sales_anomalies_statistical(df: pd.DataFrame) -> pd.DataFrame:
    daily_sales = prepare_daily_sales(df).copy()

    mean_sales = daily_sales["sales"].mean()
    std_sales = daily_sales["sales"].std()

    upper_bound = mean_sales + 2 * std_sales
    lower_bound = mean_sales - 2 * std_sales

    daily_sales["anomaly_flag"] = (
        (daily_sales["sales"] > upper_bound) |
        (daily_sales["sales"] < lower_bound)
    )

    daily_sales["anomaly_type"] = "Normal"
    daily_sales.loc[daily_sales["sales"] > upper_bound, "anomaly_type"] = "Spike"
    daily_sales.loc[daily_sales["sales"] < lower_bound, "anomaly_type"] = "Drop"

    return daily_sales


def detect_sales_anomalies_isolation_forest(df: pd.DataFrame) -> pd.DataFrame:
    daily_sales = prepare_daily_sales(df).copy()

    daily_sales["day_of_week"] = daily_sales["order_day"].dt.dayofweek
    daily_sales["day_of_month"] = daily_sales["order_day"].dt.day
    daily_sales["month"] = daily_sales["order_day"].dt.month
    daily_sales["rolling_mean_7"] = daily_sales["sales"].rolling(window=7, min_periods=1).mean()
    daily_sales["rolling_std_7"] = daily_sales["sales"].rolling(window=7, min_periods=1).std().fillna(0)

    feature_cols = ["sales", "day_of_week", "day_of_month", "month", "rolling_mean_7", "rolling_std_7"]
    X = daily_sales[feature_cols]

    model = IsolationForest(
        n_estimators=200,
        contamination=0.03,
        random_state=42
    )
    preds = model.fit_predict(X)
    scores = model.decision_function(X)

    daily_sales["iforest_flag"] = preds
    daily_sales["iforest_anomaly"] = daily_sales["iforest_flag"].apply(lambda x: 1 if x == -1 else 0)
    daily_sales["iforest_score"] = scores

    daily_sales["iforest_type"] = "Normal"
    daily_sales.loc[
        (daily_sales["iforest_anomaly"] == 1) & (daily_sales["sales"] > daily_sales["rolling_mean_7"]),
        "iforest_type"
    ] = "Spike"
    daily_sales.loc[
        (daily_sales["iforest_anomaly"] == 1) & (daily_sales["sales"] <= daily_sales["rolling_mean_7"]),
        "iforest_type"
    ] = "Drop"

    return daily_sales


def detect_sales_anomalies_timeseries(df: pd.DataFrame) -> pd.DataFrame:
    daily_sales = prepare_daily_sales(df).copy()

    ts = daily_sales.set_index("order_day")["sales"].asfreq("D").fillna(0)

    model = ExponentialSmoothing(
        ts,
        trend="add",
        seasonal=None
    ).fit()

    fitted_values = model.fittedvalues
    result = pd.DataFrame({
        "order_day": fitted_values.index,
        "sales": ts.values,
        "expected_sales": fitted_values.values
    })

    result["residual"] = result["sales"] - result["expected_sales"]
    residual_std = result["residual"].std()

    upper_bound = 2 * residual_std
    lower_bound = -2 * residual_std

    result["ts_anomaly"] = (
        (result["residual"] > upper_bound) |
        (result["residual"] < lower_bound)
    ).astype(int)

    result["ts_type"] = "Normal"
    result.loc[result["residual"] > upper_bound, "ts_type"] = "Spike"
    result.loc[result["residual"] < lower_bound, "ts_type"] = "Drop"

    return result.reset_index(drop=True)