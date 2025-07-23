import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

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

# Visualizations:
if section == "Monthly Revenue Trends":
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["month_year"],
        y=df["total_revenue"],
        name="Total Revenue",
        marker_color='steelblue',
        yaxis="y1"
    ))

    fig.add_trace(go.Scatter(
        x=df["month_year"],
        y=df["avg_order"],
        name="Average Order",
        mode="lines+markers",
        marker_color='orange',
        yaxis="y2"
    ))

    fig.update_layout(
        title="Monthly Revenue Trends",
        xaxis_title="Month",
        yaxis=dict(title="Total Revenue", side='left'),
        yaxis2=dict(title="Average Order", overlaying='y', side='right'),
        legend=dict(orientation="h")
    )

    st.plotly_chart(fig, use_container_width=True)

elif section == "Top 15 Best-Selling Products":
    fig = px.bar(
        df.sort_values("total_revenue"),  # Show highest at the top
        x="total_revenue",
        y="description",
        orientation='h',
        title="Top 15 Best-Selling Products",
        labels={"total_revenue": "Total Revenue", "description": "Product"}
    )

    st.plotly_chart(fig, use_container_width=True)

elif section == "RFM Analysis":
    # Create Recency-Frequency Segment
    df['recency_segment'] = pd.qcut(df['recency_score'], q=5, labels=False)
    df['frequency_monetary_score'] = (df['monetary_score'] + df['frequency_score']) / 2
    df['frequency_monetary_segment'] = pd.qcut(df['frequency_monetary_score'], q=5, labels=False)
    

    # Build Pivot Table: Count of Customers
    rfm_pivot = df.pivot_table(
        index='recency_segment',
        columns='frequency_monetary_segment',
        values='customer_id',
        aggfunc='count'
    ).fillna(0)

    # Plot Heatmap using Seaborn
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(rfm_pivot, annot=True, fmt=".0f", cmap="YlOrRd", linewidths=.5, ax=ax)
    ax.set_xlabel("Frequency + Monetary Segment (Mean)")
    ax.set_ylabel("Recency Segment")
    ax.set_title("RFM Matrix – Customers Concentration")

    st.pyplot(fig)

elif section == "Average Order by Country":
    fig = px.choropleth(
        df,
        locations="country",
        locationmode="country names",
        color="avg_order",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.speed,
        title="Average Order Value by Country"
    )
    
    fig.update_layout(
        width=1200,
        height=700, 
        plot_bgcolor="#ffffff",
        paper_bgcolor="#0f1116",
        font_color="white",
        geo=dict(
            bgcolor="#0f1116"
        )
)
    fig.update_geos(fitbounds="locations")
    st.plotly_chart(fig, use_container_width=True)