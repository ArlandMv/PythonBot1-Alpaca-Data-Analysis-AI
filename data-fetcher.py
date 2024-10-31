import requests
import pandas as pd
from datetime import datetime
import os
import json
from time import time
from concurrent.futures import ThreadPoolExecutor
from config import ALPACA_CONFIG, PROD_URL


# Configuration
API_KEY = ALPACA_CONFIG["API_KEY"]
SECRET_KEY = ALPACA_CONFIG["API_SECRET"]
# BASE_URL = "https://data.alpaca.markets/v2"
BASE_URL = ALPACA_CONFIG["ENDPOINT"] #without the version

def fetch_stock_data(symbol, start_date, end_date):
    """Fetch historical data for a single stock"""
    headers = {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": SECRET_KEY
    }

    params = {
        "start": start_date.strftime("%Y-%m-%d"),
        "end": end_date.strftime("%Y-%m-%d"),
        "timeframe": "1Day",
        "adjustment": "raw"
    }

    endpoint = f"{BASE_URL}/stocks/{symbol}/bars"

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        return symbol, response.json()
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return symbol, None

def process_and_save_data(symbol, data, save_path="data"):
    """Process and save data for a single stock"""
    if not data or 'bars' not in data:
        print(f"No data available for {symbol}")
        return

    # Convert to DataFrame
    df = pd.DataFrame(data['bars'])

    # Process the data
    df['t'] = pd.to_datetime(df['t'])
    df = df.rename(columns={
        't': 'timestamp',
        'o': 'open',
        'h': 'high',
        'l': 'low',
        'c': 'close',
        'v': 'volume',
        'n': 'trade_count',
        'vw': 'vwap'
    })

    # Save as both CSV and Parquet
    os.makedirs(f"{save_path}/processed", exist_ok=True)

    # Save as CSV for easy viewing
    csv_file = f'{save_path}/processed/{symbol}_data.csv'
    df.to_csv(csv_file, index=False)

    # Save as Parquet for efficient storage
    parquet_file = f'{save_path}/processed/{symbol}_data.parquet'
    df.to_parquet(parquet_file, compression='snappy')

    print(f"\nSaved {symbol} data:")
    print(f"CSV: {csv_file}")
    print(f"Parquet: {parquet_file}")
    print("\nSample data:")
    print(df.head())

    return {
        'symbol': symbol,
        'days': len(df),
        'start': df['timestamp'].min().strftime('%Y-%m-%d'),
        'end': df['timestamp'].max().strftime('%Y-%m-%d'),
        'avg_volume': int(df['volume'].mean())
    }

def fetch_multiple_stocks(symbols, start_date, end_date, max_workers=5):
    """Fetch data for multiple stocks in parallel"""
    print(f"Fetching data for {len(symbols)} symbols...")
    start_time = time()

    # Create directories
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # Fetch data in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(fetch_stock_data, symbol, start_date, end_date)
            for symbol in symbols
        ]

        results = []
        for future in futures:
            symbol, data = future.result()
            if data:
                # Save raw data
                with open(f'data/raw/{symbol}_raw.json', 'w') as f:
                    json.dump(data, f, indent=4)

                # Process and save data
                stats = process_and_save_data(symbol, data)
                if stats:
                    results.append(stats)

    # Save summary
    end_time = time()
    summary = {
        'fetch_time_seconds': round(end_time - start_time, 2),
        'symbols_processed': len(results),
        'results': results
    }

    with open('data/processed/summary.json', 'w') as f:
        json.dump(summary, f, indent=4)

    print(f"\nCompleted in {summary['fetch_time_seconds']} seconds")
    return summary

if __name__ == "__main__":
    # Example usage
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    summary = fetch_multiple_stocks(symbols, start_date, end_date)

    print("\nProcessing Summary:")
    for result in summary['results']:
        print(f"\n{result['symbol']}:")
        print(f"  Period: {result['start']} to {result['end']}")
        print(f"  Trading days: {result['days']}")
        print(f"  Average daily volume: {result['avg_volume']:,}")