-- Monthly sales summary
SELECT
    order_month,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales_orders
GROUP BY order_month
ORDER BY order_month;

-- Top products
SELECT
    product_name,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit
FROM sales_orders
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;

-- Sales by region
SELECT
    region,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit
FROM sales_orders
GROUP BY region
ORDER BY total_sales DESC;

-- Sales by category
SELECT
    category,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit
FROM sales_orders
GROUP BY category
ORDER BY total_sales DESC;

-- Customer segment performance
SELECT
    segment,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM sales_orders
GROUP BY segment
ORDER BY total_sales DESC;
