# Inflation vs E-Commerce Sales Data Warehouse

## Project Overview

This project combines Brazilian e-commerce sales data from the Olist dataset with Brazil CPI data obtained through the FRED API to build a small analytical data warehouse.

The main objective is to analyze how sales behavior changes over time in relation to CPI trends using a dimensional warehouse model and SQL analysis.

The project follows a complete ETL workflow:

1. Extract raw data from CSV files and API
2. Transform and model the data into fact and dimension tables
3. Load the warehouse into PostgreSQL
4. Perform analytical SQL queries

---

# Technologies Used

- Python (SQLAlchemy, Requests, Pandas)
- PostgreSQL
- SQL
- FRED API

---

# Data Sources

## 1. Olist Brazilian E-Commerce Dataset

Dataset used for sales and product information:

[https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

Tables used:

- orders
- order_items
- products
- customers

---

## 2. Brazil CPI Data (FRED API)

FRED series used:

[https://fred.stlouisfed.org/series/CPALTT01BRM659N](https://fred.stlouisfed.org/series/CPALTT01BRM659N)

The API provides monthly CPI-related data used for time-series analysis.

## Sample Data Notice

To keep the repository lightweight and GitHub-friendly, only sample datasets are included in the repository.

The original Olist datasets are significantly larger and are not uploaded to GitHub.

## The data/sample/ directory contains small representative subsets of the processed tables used for demonstration and testing purposes.

# Project Structure

```text
Inflation-Sales/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── sql/
│   └── analysis_queries.sql
│
├── config/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ETL Pipeline

## Extract

The extract phase:

- Loads raw Olist CSV datasets
- Connects to the FRED API
- Retrieves CPI data
- Stores raw files locally

Main outputs:

- customers_raw.csv
- orders_raw.csv
- order_items_raw.csv
- products_raw.csv
- CPI_raw.csv

---

## Transform

The transform phase:

- Cleans and filters relevant columns
- Converts timestamps into datetime objects
- Extracts year and month from order timestamps
- Creates dimension tables
- Builds analytical fact tables
- Aggregates monthly sales metrics

Dimension tables:

- dim_date
- dim_product
- dim_customer

Fact tables:

- fact_sales
- fact_cpi

---

## Load

The load phase:

- Creates warehouse tables in PostgreSQL
- Defines primary and foreign keys

The warehouse follows a star-schema style structure.

---

# Data Warehouse Model

## Dimensions

### dim_date

| Column  |
| ------- |
| date_id |
| year    |
| month   |

---

### dim_product

| Column        |
| ------------- |
| product_id    |
| category_name |

---

### dim_customer

| Column         |
| -------------- |
| customer_id    |
| customer_state |

---

## Fact Tables

### fact_sales

| Column       |
| ------------ |
| date_id      |
| product_id   |
| total_sales  |
| total_orders |

Each row represents:

> One product category aggregated for one month.

---

### fact_cpi

| Column    |
| --------- |
| date_id   |
| cpi_value |

Each row represents:

> One CPI value for one month.

---

# Relationship Between Datasets

Both fact tables connect through the shared time dimension:

```text
fact_sales
    ↓
 dim_date
    ↑
fact_cpi
```

This allows time-based analysis between:

- sales behavior
- CPI trends

---

# Example Analytical Questions

Some example business questions explored with SQL:

- What was the total monthly sales revenue?
- Which months had the highest CPI values?
- Which product categories generated the most revenue during high CPI months?
- Which months had high CPI but below-average sales?

---

# Example SQL Query

```sql
SELECT
    dd.year,
    dd.month,
    dp.category_name,
    fc.cpi_value,
    ROUND(SUM(fs.total_sales)::numeric, 2) AS total_revenue
FROM fact_sales fss

JOIN dim_date dd
    ON fss.date_id = dd.date_id

JOIN fact_cpi fc
    ON fss.date_id = fc.date_id

JOIN dim_product dp
    ON fss.product_id = dp.product_id

GROUP BY
    dd.year,
    dd.month,
    dp.category_name,
    fc.cpi_value

ORDER BY
    fc.cpi_value DESC,
    total_revenue DESC;
```

---

# Key Skills Demonstrated

- ETL pipeline development
- API data extraction
- Data cleaning and transformation
- Dimensional modeling
- Fact and dimension table design
- PostgreSQL warehouse loading
- Analytical SQL queries
- Multi-source data integration

---

# Future Improvements

Possible future extensions:

- Containerize the project with Docker
- Add dashboards using Power BI or Tableau
- Calculate inflation rates from CPI changes
- Add more economic indicators

---

# Author

Rodrigo Carranza

GitHub: https://github.com/rogos14
