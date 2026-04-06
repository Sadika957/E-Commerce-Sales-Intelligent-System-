import sqlite3
import pandas as pd
from pathlib import Path


def get_db_connection(db_path: str = "../data/ecommerce.db"):
    Path("../data").mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    return conn


def run_schema(conn, schema_path: str = "../sql/schema.sql"):
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()


def load_dataframe_to_sql(df: pd.DataFrame, conn, table_name="sales_orders"):
    df.to_sql(table_name, conn, if_exists="append", index=False)


def run_query(conn, query):
    return pd.read_sql_query(query, conn)


def run_query_file(conn, file_path="../sql/analytics_queries.sql"):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    queries = [q.strip() for q in content.split(";") if q.strip()]
    results = []

    for query in queries:
        df = pd.read_sql_query(query, conn)
        results.append(df)

    return results
