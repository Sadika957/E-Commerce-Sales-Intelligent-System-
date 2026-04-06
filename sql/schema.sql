DROP TABLE IF EXISTS sales_orders;

CREATE TABLE sales_orders (
    row_id INTEGER,
    order_id TEXT,
    order_date TEXT,
    ship_date TEXT,
    ship_mode TEXT,
    customer_id TEXT,
    customer_name TEXT,
    segment TEXT,
    country TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    region TEXT,
    product_id TEXT,
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    sales REAL,
    quantity INTEGER,
    discount REAL,
    profit REAL,
    profit_margin REAL,
    order_year INTEGER,
    order_month TEXT,
    order_day TEXT
);
