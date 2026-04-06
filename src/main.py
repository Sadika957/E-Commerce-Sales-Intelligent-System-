import os
import pandas as pd

from ingest import load_data
from preprocess import preprocess_data
from kpi_analysis import generate_kpis, monthly_sales_summary, top_products, top_categories
from anomaly_detection import (
    detect_sales_anomalies_statistical,
    detect_sales_anomalies_isolation_forest,
    detect_sales_anomalies_timeseries
)
from forecasting import forecast_sales
from visualize import (
    plot_monthly_sales,
    plot_monthly_profit,
    plot_sales_anomalies,
    plot_sales_forecast,
    plot_iforest_anomalies,
    plot_timeseries_anomalies
)
from database import (
    get_db_connection,
    run_schema,
    load_dataframe_to_sql,
    run_query_file
)


def main():
    input_path = "C:/Users/DELL/Desktop/ecommerce-sales-intelligent-system/data/raw/ecommerce_sales.csv"
    processed_path = "C:/Users/DELL/Desktop/ecommerce-sales-intelligent-system/data/processed/cleaned_ecommerce_sales.csv"

    os.makedirs("C:/Users/DELL/Desktop/ecommerce-sales-intelligent-system/data/processed", exist_ok=True)
    os.makedirs("C:/Users/DELL/Desktop/ecommerce-sales-intelligent-system/outputs/tables", exist_ok=True)
    os.makedirs("C:/Users/DELL/Desktop/ecommerce-sales-intelligent-system/outputs/charts", exist_ok=True)
    os.makedirs("outputs/sql", exist_ok=True)

    df = load_data(input_path)
    df = preprocess_data(df)
    df.to_csv(processed_path, index=False)

    # KPI outputs from Python
    kpis = generate_kpis(df)
    pd.DataFrame([kpis]).to_csv("outputs/tables/kpi_summary.csv", index=False)

    monthly_summary = monthly_sales_summary(df)
    monthly_summary.to_csv("outputs/tables/monthly_sales_summary.csv", index=False)

    product_summary = top_products(df)
    product_summary.to_csv("outputs/tables/top_products.csv", index=False)

    category_summary = top_categories(df)
    category_summary.to_csv("outputs/tables/top_categories.csv", index=False)

    # Anomaly detection outputs
    statistical_anomalies = detect_sales_anomalies_statistical(df)
    statistical_anomalies.to_csv("outputs/tables/sales_anomalies_statistical.csv", index=False)

    iforest_anomalies = detect_sales_anomalies_isolation_forest(df)
    iforest_anomalies.to_csv("outputs/tables/sales_anomalies_iforest.csv", index=False)

    ts_anomalies = detect_sales_anomalies_timeseries(df)
    ts_anomalies.to_csv("outputs/tables/sales_anomalies_timeseries.csv", index=False)

    # Forecasting output
    forecast_df = forecast_sales(df, forecast_periods=30)
    forecast_df.to_csv("outputs/tables/sales_forecast.csv", index=False)

    # Charts
    plot_monthly_sales(df, "outputs/charts")
    plot_monthly_profit(df, "outputs/charts")
    plot_sales_anomalies(statistical_anomalies, "outputs/charts")
    plot_iforest_anomalies(iforest_anomalies, "outputs/charts")
    plot_timeseries_anomalies(ts_anomalies, "outputs/charts")
    plot_sales_forecast(df, forecast_df, "outputs/charts")

    # SQL warehouse + analytics
    conn = get_db_connection("C:/Users/DELL/Desktop/ecommerce-sales-intelligent-system/data/ecommerce.db")
    run_schema(conn, "C:/Users/DELL/Desktop/ecommerce-sales-intelligent-system/sql/schema.sql")
    load_dataframe_to_sql(df, conn, "sales_orders")

    sql_results = run_query_file(conn, "C:/Users/DELL/Desktop/ecommerce-sales-intelligent-system/sql/analytics_queries.sql")

    sql_output_names = [
        "sql_monthly_sales_summary.csv",
        "sql_top_products.csv",
        "sql_sales_by_region.csv",
        "sql_sales_by_category.csv",
        "sql_segment_performance.csv"
    ]

    for result_df, file_name in zip(sql_results, sql_output_names):
        result_df.to_csv(f"outputs/sql/{file_name}", index=False)

    conn.close()

    print("Project pipeline executed successfully.")
    print("Charts saved in outputs/charts/")
    print("Tables saved in outputs/tables/")
    print("SQL outputs saved in outputs/sql/")
    print("Database created at data/ecommerce.db")
    print("KPI Summary:", kpis)
    print("Statistical anomalies detected:", int(statistical_anomalies["anomaly_flag"].sum()))
    print("Isolation Forest anomalies detected:", int(iforest_anomalies["iforest_anomaly"].sum()))
    print("Time-series anomalies detected:", int(ts_anomalies["ts_anomaly"].sum()))


if __name__ == "__main__":
    main()