import alpaca_trade_api as tradeapi
import pandas as pd

import pandas as pd
from datetime import datetime
import os
import json
import requests
from config import ALPACA_CONFIG, PAPER_TRADING, PROD_URL


# Define your stock symbols
us_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
BASE_URL = PROD_URL

# Replace with your API keys from Alpaca dashboard
API_KEY = "YOUR_API_KEY"
SECRET_KEY = "YOUR_SECRET_KEY"
API_KEY = ALPACA_CONFIG["API_KEY"]
SECRET_KEY = ALPACA_CONFIG["API_SECRET"]

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')


# Create directories if they don't exist
os.makedirs("../data/raw", exist_ok=True)
os.makedirs("../data/processed", exist_ok=True)

# Function to get historical data for a long-term strategy
def get_historical_bars(symbols, timeframe="day", start="2023-01-01", end="2023-12-31"):
    historical_data = {}
    for symbol in symbols:
        barset = api.get_barset(symbol, timeframe, start=start, end=end)
        historical_data[symbol] = barset[symbol]._raw
    return historical_data

def main():

    # Get historical data for the defined stocks
    historical_data = get_historical_bars(us_stocks)

    # Display the data and save it
    for symbol, data in historical_data.items():
        print(f"\n{symbol} Historical Data:")
        df = pd.DataFrame(data)
        print(df)  # Print data to console

        # Save both raw and readable formats
        df.to_csv(f"{symbol}_raw.csv", index=False)  # Save raw data
        readable_df = df[['t', 'c']]  # Time and Close for readability
        readable_df.to_csv(f"{symbol}_readable.csv", index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    trade=False
    main()