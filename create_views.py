from google.cloud import bigquery

from dotenv import load_dotenv
import os

from retail.bigquery import BigQuery

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
DATASET = "online_retail_uci_roller"
DATASET_ID = f"{PROJECT_ID}.{DATASET}"

bq = BigQuery(PROJECT_ID, DATASET)

query = f"""
SELECT
ft.product_id,
p.description,
DATE_DIFF(CURRENT_DATETIME(), MAX(d.datetime), DAY) as recency,
COUNT(ft.quantity) AS num_sales,
SUM(ft.quantity * p.price) AS revenue
FROM `{DATASET_ID}.fact_transactions` AS ft
JOIN `{DATASET_ID}.products` AS p ON p.product_id = ft.product_id
JOIN `{DATASET_ID}.dates` AS d ON d.date_id = ft.date_id
GROUP BY ft.product_id, p.description
ORDER BY revenue DESC
LIMIT 500;
"""
bq.create_view('top_products', query)

query = f"""
WITH cost AS (
SELECT ft.*,
ft.quantity * p.price AS revenue
FROM `{DATASET_ID}.fact_transactions` AS ft
JOIN `{DATASET_ID}.products` AS p ON p.product_id = ft.product_id
)
SELECT
c.customer_id,
DATE_DIFF(CURRENT_DATETIME(), MAX(d.datetime), DAY) as recency,
COUNT(ft.quantity) AS num_sales,
SUM(ft.revenue) AS revenue
FROM cost AS ft
JOIN `{DATASET_ID}.products` AS p ON p.product_id = ft.product_id
JOIN `{DATASET_ID}.dates` AS d ON d.date_id = ft.date_id
JOIN `{DATASET_ID}.customers` AS c ON c.customer_id = ft.customer_id
WHERE c.customer_id != "nan"
GROUP BY c.customer_id
ORDER BY revenue DESC
LIMIT 500;
"""
bq.create_view('top_customers', query)

query = f"""
SELECT CAST(d.datetime AS DATE) AS date, d.year, d.month, d.day, SUM(ft.quantity) AS sales
FROM `{DATASET_ID}.fact_transactions` AS ft
JOIN `{DATASET_ID}.dates` AS d ON d.date_id = ft.date_id
GROUP BY CAST(d.datetime AS DATE), d.year, d.month, d.day;"""
bq.create_view('daily_sales', query)

query = f"""
SELECT countries.country, countries.dist_from_uk, SUM(ft.quantity) AS sales
FROM `{DATASET_ID}.fact_transactions` AS ft
JOIN `{DATASET_ID}.customers` AS cust ON cust.customer_id = ft.customer_id
JOIN `{DATASET_ID}.countries` AS countries ON cust.country_id = countries.country_id
GROUP BY countries.country, countries.dist_from_uk
ORDER BY sales DESC;"""
bq.create_view('country_sales', query)
