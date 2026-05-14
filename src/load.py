from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

base_path = Path(r"Inflation-Sales\data\processed")

dim_date        = pd.read_csv(base_path / "dim_date.csv")
dim_customer    = pd.read_csv(base_path / "dim_customer.csv")
dim_product     = pd.read_csv(base_path / "dim_product.csv")

fact_cpi        = pd.read_csv(base_path / "fact_cpi.csv")
fact_sales      = pd.read_csv(base_path / "fact_sales.csv")

engine = create_engine("postgresql://postgres:drakariuros14@localhost:5432/Inflation_sales_analysis")
print("Connected to PostgreSQL")

with engine.begin() as conn:
    #Drop existing tables
    conn.execute(text("""
        DROP TABLE IF EXISTS fact_sales CASCADE;
        DROP TABLE IF EXISTS fact_cpi CASCADE;
        DROP TABLE IF EXISTS dim_date CASCADE;
        DROP TABLE IF EXISTS dim_product CASCADE;
        DROP TABLE IF EXISTS dim_customer CASCADE;
    """))
    
    conn.execute(text("""
        CREATE TABLE dim_date (
            date_id INT PRIMARY KEY,
            year INT,
            month INT
        );
    """))

    conn.execute(text("""
        CREATE TABLE dim_product (
            product_id TEXT PRIMARY KEY,
            category_name TEXT
        );               
    """))

    conn.execute(text("""
        CREATE TABLE dim_customer (
            customer_id TEXT PRIMARY KEY,
            customer_state TEXT
        );              
    """))

    conn.execute(text("""
        CREATE TABLE fact_sales (
            date_id INT ,
            product_id TEXT,
            total_sales FLOAT,
            total_orders INT,
            
            FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
            FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
        );               
    """))

    conn.execute(text("""
        CREATE TABLE fact_cpi (
            date_id INT,
            cpi_value FLOAT,
                      
            FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
        );                
    """))

# Load dimensions
dim_date.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False
)

dim_customer.to_sql(
    "dim_customer",
    engine,
    if_exists="append",
    index=False
)

dim_product.to_sql(
    "dim_product",
    engine,
    if_exists="append",
    index=False
)

# Load fact tables

fact_sales.to_sql(
    "fact_sales",
    engine,
    if_exists="append",
    index=False
)

fact_cpi.to_sql(
    "fact_cpi",
    engine,
    if_exists="append",
    index=False
)