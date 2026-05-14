import requests
import pandas as pd
from pathlib import Path

# Load file paths
input_path      = Path("Inflation-Sales\data\sample")
output_path     = Path(r"Inflation-Sales\data\raw")
output_path.mkdir(parents=True, exist_ok=True)

# Read csv files
order_file_df           = pd.read_csv(input_path / "orders.csv")
products_file_df        = pd.read_csv(input_path / "products.csv")
customers_file_df       = pd.read_csv(input_path / "customers.csv")
order_items_file_df     = pd.read_csv(input_path / "order_items.csv")


# Extract API data 
API_KEY = "9896132ba009fcde5ec075c239997148"

base_url = "https://api.stlouisfed.org/fred/"
obs_endpoint = "series/observations"
series_id = "CPALTT01BRM659N"
start_date = '2017-01-01'
end_date = '2018-12-31'
obs_params = {
    'series_id': series_id,
    'api_key': API_KEY,
    'file_type': 'json',
    'observation_start': start_date,
    'observation_end': end_date,
}

response = requests.get(base_url + obs_endpoint, params=obs_params)

if response.status_code == 200:
    data = response.json()
    obs_df = pd.DataFrame(data["observations"])
    cpi_df = obs_df[["date", "value"]]


# Save raw data to folder
order_file_df.sample(100).to_csv(output_path / "orders_raw.csv", index=False)
products_file_df.sample(100).to_csv(output_path / "products_raw.csv", index=False)
customers_file_df.sample(100).to_csv(output_path / "customers_raw.csv", index=False)
order_items_file_df.sample(100).to_csv(output_path / "order_items_raw.csv", index=False)

cpi_df.to_csv(output_path / "CPI_raw.csv", index=False)