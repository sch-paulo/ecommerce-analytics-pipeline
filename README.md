### English [(Versão em português aqui)](README-pt.md)

# Ecommerce Analytics Pipeline

[![UV](https://img.shields.io/badge/uv-261231?logo=UV&logoColor=de5fea)](https://github.com/astral-sh/uv)
[![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Jupyter Notebook](https://img.shields.io/badge/Jupyter%20Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-6599c3?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Pandas](https://img.shields.io/badge/-Pandas-130654?&logo=pandas)](https://pandas.pydata.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-667566?logo=sqlalchemy&logoColor=d72407)](https://www.sqlalchemy.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)

<p align="center">
  <img src="img\ecommerce.png" alt="Cover image">
</p>

## Project Overview

A simple project developed to create a pipeline for data collection, database setup, analyze and visualize retail data.  
**Goal:** Simulate a real world task in order to improve my end-to-end data engineering skills.
<br>

## Data Sources

- **E-Commerce Data**: Available [here on Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data).
- Also provided on [`data` folder](data) on ZIP format.
<br>

## Key Features & Components

### 1. Data Collection & Cleaning

- Pull sales data from the Kaggle dataset (publicly available with link [above](#data-sources))
- Use [Jupyter Notebooks](notebooks) to explore and analyze initially the data 
- Clean the data — handle missing values, remove duplicates, fix data types
- Document the quality issues found

### 2. Database Setup

- Set up a PostgreSQL database on Docker
- Design and create appropriate tables with proper indexing
- Load cleaned data into the database

### 3. Analytics Queries

- SQL queries to answer some business questions:
    - Monthly revenue trends
    - Top 15 best-selling products
    - Average order value by customer country
    - Customer segmentation by purchase behavior (RFM Analysis)    

### 4. Simple Dashboard

- Basic dashboard using Streamlit
- Simple visualizations with the results of the queries above

### 5. Documentation

- README with setup instructions
- Code comments when necessary
- Brief summary of key insights discovered

## Technologies Used

- **Python**: Data cleaning, processing and database connection (`pandas`, `SQLAlchemy`)
- **Jupyter Notebooks**: EDA and testing data handling
- **PostgreSQL**: Data storage
- **Streamlit**: Data visualization
- **Docker**: Containerization of all the project's steps
<br>

## How to Run

### Prerequisites
Make sure you have the following components installed: <br>
- [Docker](https://docs.docker.com/get-started/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
<br>

### Running the project
1. **Clone the repository**
   ```sh
   git clone https://github.com/sch-paulo/ecommerce-analytics-pipeline.git
   cd ecommerce-analytics-pipeline
   ```

2. **Set up a environment variables file**
- On project's root folder, create a `.env` file containing the following credentials:
    - `POSTGRES_DB`=your_db_name
    - `POSTGRES_USER`=your_user
    - `POSTGRES_PASSWORD`=your_password
- I have provided a sample file so you can check its structure (you will still need to rename it to make it usable).

3. **Start the application using Docker Compose**
    ```sh
    docker-compose up --build
    ```

    - One annoying part of the process is that the dashboard container takes a while to load, as it needs to wait for the ETL container to finish the entire process, and ingesting all the data into the database takes a few minutes.

4. **Access the app**
- Once running, access it through the link http://localhost:8501 (this is the port I used for the application on `docker-compose.yml`, if you change it, the link will also need to be changed).

5. **Visualize**
- The app displays visuals separated by tabs, with each tab representing a query.

6. **Accessing the data**
- On the SGBD of your preference (DBeaver, pgAdmin, etc.), create a connection using the following credentials:
    - **Host name:**  `localhost` (`postgres` for accesses inside container) <br> 
    - **Port:** `5433` (pay attention because it's not the same port used by the container)<br> 
- From here, use the same credentials you put inside the `.env` file.
    - **Maintenance database:** `your_db_name` <br> 
    - **Username:** `your_user` <br> 
    - **Password:** `your_password`
<br>

## Results & Insights
### 1. Monthly revenue trends <br /> 
The period from December 2010 to December 2011 showed moderated volatility. Revenue peaked in November 2011 at $1,456,145.80, driven by the highest monthly growth of 49.34% in September and a strong increase of 36.17% in November. Speaking about bad months, January (-25.21%) and April 2011 (-27.81%) saw the most significant declines from the period.

### 2. Top 15 best selling products <br /> 
With over $164,000 in revenue, the *REGENCY CAKESTAND 3 TIER* product is the clear leader in the best-seller ranking. Completing the podium are *PARTY BUNTING*, with over $98,000, and *WHITE HANGING HEART T-LIGHT HOLDER*, with approximately $97,800 in revenue. The diversity of products in the top 15 shows a variety of items that generate revenue, from party supplies to home décor items.

### 3. Average order by country <br /> 
Although the United Kingdom has an average order value of $347.72 (not the highest), it is the country that generates the most revenue, with a total of $8 million, representing an impressive 84.3% of total revenue. In contrast, the Netherlands has the highest average order value of $2,818.43, but its total revenue of less than $285,000 represents only 2.9% of the total, indicating a lower order volume but a very high average ticket. From the 37 countries with orders, only 18 of them represent at least more than 0.1% of revenue (more than $10,000).

### 4. Customer segmentation <br /> 
For this analysis, we divided each RFM metric (Recency of days since last purchase, Frequency of purchases, and total Monetary Value spent) into 5 quintiles, assigning scores from 1 to 5 for each, where 5 represents the best performance. For Recency, higher scores were given to customers with fewer days since their last purchase. For Frequency and Monetary Value, higher scores were assigned to customers with higher frequency and higher spending. The sum of these three scores was used to categorize customers into distinct segments.

**Customer segmentation and distribution**:
| Segment             | % of Customers | Total Customers | Avg. Recency (Days) | Avg. Frequency | Avg. Monetary Value |
|---------------------|----------------|-----------------|---------------------|----------------|---------------------|
| Champions           | 21.6%          | 945             | 12.4                | 14.1           | $6,215.23           |
| Loyal Customers     | 17.3%          | 758             | 42.8                | 4.6            | $1,403.79           |
| Potential Loyalists | 22.6%          | 989             | 77.2                | 2.5            | $706.68             |
| At Risk             | 17.0%          | 742             | 104.5               | 1.7            | $391.71             |
| Lost                | 21.5%          | 938             | 221.8               | 1.2            | $203.05             |


- **Champions**: These are the best customers. With an average recency of only 12 days, a high frequency of more than 14 purchases, and an average monetary value of over $6,000, they are the most recent, most frequent, and highest spending customers. They are the foundation of the business and deserve special attention for retention and rewards.

- **Loyal Customers**: Customers who buy regularly and spend a good amount. With an average recency of 43 days, a frequency of 4.6 purchases, and an average spend of $1,403, they are valuable customers who respond well to personalized offers and loyalty programs.

- **Potential Loyalists**: These customers have purchased recently, but not yet with the same frequency or value as loyal customers. With an average recency of 77 days, 2.5 purchases, and an average spend of $707, they have good potential to become loyal customers with the right engagement, such as campaigns to encourage repeat purchases.

- **At Risk**: Customers who have not purchased in a while but have had a good history. With an average recency of 104 days, low frequency (1.7 purchase), and an average monetary value of $392, they need re-engagement campaigns to prevent them from becoming “Lost”.

- **Lost**: These represent a significant portion of the customer base that has not purchased in a long time. With an average recency of 222 days, very low frequency (1.2 purchase), and an average spend of only $203, the strategy for this group may be to try to reactivate them with very aggressive offers, or to focus efforts on other segments.
<br>

## Project Structure
```graphql
ecommerce-analytics-pipeline/
├── app/                     # Dashboard app
│   ├── Dockerfile
│   ├── dashboard.py
│   └── requirements.txt
├── config/                  # Configuration modules
│   └── country_map.py
├── data/                    # Input data and raw files
│   ├── data.csv
│   └── ecommerce-data.zip
├── notebooks/               # Jupyter notebooks for EDA and cleaning
│   ├── 01_data_exploration.ipynb
│   └── 02_data_cleaning.ipynb
├── schema/                  # Database schema definitions
│   └── models.py
├── scripts/                 # SQL queries used for analytics
│   ├── 01_monthly_revenue_trends.sql
│   ├── 02_top_best_selling.sql
│   ├── 03_average_order_by_country.sql
│   └── 04_customer_segmentation.sql
├── src/                     # Core ETL pipeline scripts
│   ├── Dockerfile
│   ├── clean_data.py
│   ├── database.py
│   ├── load_to_db.py
│   └── requirements.txt
├── .env                     # Environment variables file
├── README.md                # Project documentation (en version)
├── README-pt-br.md          # Project documentation (pt-br version)
├── docker-compose.yml       # Container orchestration
└── requirements_project.txt # Project-wide dependencies
```