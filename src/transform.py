import pandas as pd
from pathlib import Path
import json

input_path      = Path(r"Inflation-Sales\data\raw")
output_path     = Path(r"Inflation-Sales\data\processed")

customers_df    = pd.read_csv(input_path / "customers_raw.csv")
order_items_df  = pd.read_csv(input_path / "order_items_raw.csv")
orders_df       = pd.read_csv(input_path / "orders_raw.csv")
products_df     = pd.read_csv(input_path / "products_raw.csv")

CPI_df          = pd.read_csv(input_path / "CPI_raw.csv")


#Extract required data
customer_df     = customers_df[["customer_id", "customer_state"]]
order_item_df   = order_items_df[["order_id", "order_item_id", "product_id", "price"]]
orders_df       = orders_df[["order_id", "customer_id", "order_purchase_timestamp"]]
products_df     = products_df[["product_id", "product_category_name"]]

orders_df["order_purchase_timestamp"] = pd.to_datetime(
    orders_df["order_purchase_timestamp"])

orders_df["year"]   = orders_df["order_purchase_timestamp"].dt.year
orders_df["month"]  = orders_df["order_purchase_timestamp"].dt.month

print(orders_df[["year", "month"]].head())
# Create dimension tables
dim_date = (
    orders_df[["year", "month"]]
    .drop_duplicates()
    .sort_values(["year", "month"])
    .reset_index(drop=True)
)

dim_date["date_id"] = dim_date.index + 1
dim_date = dim_date[["date_id", "year", "month"]]

dim_product = (
    products_df[["product_id", "product_category_name"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_product = dim_product.rename(columns={
    "product_category_name": "category_name"})

dim_customer = (
    customer_df[["customer_id", "customer_state"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Create fact sales
sales_df = orders_df.merge(
    order_item_df,
    on="order_id",
    how="inner"
)

sales_df = sales_df.merge(
    products_df,
    on="product_id",
    how="left"
)

sales_df = sales_df.merge(
    dim_date,
    on=["year","month"],
    how="left"
)

# Create fact table
fact_sales = (
    sales_df.groupby(
        ["date_id", "product_id"]
    )
    .agg(
        total_sales = ("price", "sum"),
        total_orders = ("order_id", "nunique")
    )
    .reset_index()
)

fact_sales["total_sales"] = (
    fact_sales["total_sales"].round(2)
)


# Create fact CPI
CPI_df["date"] = pd.to_datetime(CPI_df["date"])
CPI_df["year"] = CPI_df["date"].dt.year
CPI_df["month"] = CPI_df["date"].dt.month
CPI_df = CPI_df[CPI_df["value"] != "."]
CPI_df["value"] = CPI_df["value"].astype(float)

CPI_df = CPI_df.merge(
    dim_date,
    on=["year", "month"],
    how="left"
)

fact_cpi = CPI_df[
    ["date_id", "value"]
]

fact_cpi = fact_cpi.rename(columns={
    "value": "cpi_value"})

# Save dim and fact tables
output_path.mkdir(
    parents=True,
    exist_ok=True
)

dim_date.to_csv(
    output_path / "dim_date.csv",
    index=False
)

dim_customer.to_csv(
    output_path / "dim_customer.csv",
    index=False
)

dim_product.to_csv(
    output_path / "dim_product.csv",
    index=False
)

fact_cpi.to_csv(
    output_path / "fact_cpi.csv",
    index=False
)

fact_sales.to_csv(
    output_path / "fact_sales.csv",
    index=False
)

print("Transform stage completed.")