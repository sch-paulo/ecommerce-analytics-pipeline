import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

POSTGRES_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(POSTGRES_DATABASE_URL)

def run_query(query):
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

# --- Streamlit App ---
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Analytics Dashboard")

# Sidebar Navigation
section = st.sidebar.radio("Select Analysis", [
    "Monthly Revenue Trends",
    "Top 15 Best-Selling Products",
    "RFM Analysis",
    "Average Order by Country"
])


# --- Queries ---
queries = {}

# 1. Monthly Revenue Trends
queries["Monthly Revenue Trends"] = """
WITH orders AS(
	SELECT t.invoice_no AS order,
	       SUM(t.total_amount) AS total_value
	FROM transactions t
	GROUP BY t.invoice_no
)
SELECT TO_CHAR(i.invoice_date, 'YYYY-MM') AS month_year,
       ROUND(SUM(o.total_value)::numeric, 2) AS total_revenue,
       ROUND(AVG(o.total_value)::numeric, 2) AS avg_order
FROM orders o
JOIN invoices i ON o.order = i.invoice_no
GROUP BY month_year
ORDER BY month_year;
"""

# 2. Top 15 Best-Selling Products
queries["Top 15 Best-Selling Products"] = """
SELECT t.stock_code,
       p.description,
       ROUND(SUM(t.total_amount)::numeric, 2) AS total_revenue
FROM transactions t
JOIN products p ON t.stock_code = p.stock_code
GROUP BY t.stock_code, p.description
ORDER BY total_revenue DESC
LIMIT 15;
"""

# 3. RFM Analysis (latest and most complete)
queries["RFM Analysis"] = """
WITH customer_rfm_raw AS (
    SELECT c.customer_id,
           MAX(i.invoice_date) AS last_purchase_date,
           COUNT(DISTINCT t.invoice_no) AS frequency,
           SUM(t.total_amount)::numeric AS monetary
    FROM transactions t
    JOIN invoices i ON t.invoice_no = i.invoice_no
    JOIN customers c ON i.customer_id = c.customer_id
    WHERE c.customer_type != 'Guest'
    GROUP BY c.customer_id
),
latest_date AS (
    SELECT MAX(invoice_date) AS latest_invoice_date
    FROM invoices
),
customer_rfm AS (
    SELECT r.*,
           DATE_PART('day', l.latest_invoice_date - r.last_purchase_date) AS recency_days
    FROM customer_rfm_raw r
    CROSS JOIN latest_date l
),
rfm_scores AS (
    SELECT customer_id,
           recency_days,
           frequency,
           monetary,
           NTILE(100) OVER (ORDER BY recency_days DESC) AS recency_score,
           NTILE(100) OVER (ORDER BY frequency ASC) AS frequency_score,
           NTILE(100) OVER (ORDER BY monetary ASC) AS monetary_score
    FROM customer_rfm
)
SELECT customer_id,
       recency_days,
       frequency,
       ROUND(monetary, 2) AS monetary,
       recency_score,
       frequency_score,
       monetary_score,
       (recency_score + frequency_score + monetary_score) AS rfm_score_total
FROM rfm_scores
ORDER BY rfm_score_total DESC;
"""

# 4. Average Order by Country
queries["Average Order by Country"] = """
WITH orders AS(
	SELECT t.invoice_no AS order,
	       SUM(t.total_amount) AS total_value
	FROM transactions t
	GROUP BY t.invoice_no
)
SELECT co.country_name AS country,
       ROUND(AVG(o.total_value)::numeric, 2) AS avg_order,
       ROUND(SUM(o.total_value)::numeric, 2) AS total_revenue
FROM orders o
JOIN invoices i ON o.order = i.invoice_no
JOIN customers cu ON i.customer_id = cu.customer_id
JOIN countries co ON cu.country_id = co.country_id
GROUP BY co.country_name
ORDER BY avg_order DESC;
"""


# --- Display Section ---
st.subheader(section)

# Run and display selected query
query = queries[section]
df = run_query(query)

# Show as table
st.dataframe(df, use_container_width=True)

# Optional visualizations:
if section == "Monthly Revenue Trends":
    st.line_chart(df.set_index("month_year")["total_revenue"])

elif section == "Top 15 Best-Selling Products":
    st.bar_chart(df.set_index("description")["total_revenue"])

elif section == "RFM Analysis":
    st.bar_chart(df.set_index("customer_id")["rfm_score_total"])

elif section == "Average Order by Country":
    st.bar_chart(df.set_index("country")["avg_order"])