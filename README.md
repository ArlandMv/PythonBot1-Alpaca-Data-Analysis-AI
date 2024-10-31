# simple_trading_bot
# Alpaca Market Data Downloader

## Overview
This project provides a simple yet efficient way to download historical stock market data using Alpaca's API. It supports parallel downloads for multiple symbols and saves data in both CSV and Parquet formats for maximum flexibility.

## Features
- Parallel processing for faster data downloads
- Dual format storage (CSV and Parquet)
- Basic error handling and logging
- Summary statistics generation
- Support for custom date ranges and symbols

## Installation

### Prerequisites
- Python 3.7+
- Alpaca API credentials

### Required Packages
```bash
pip install requests pandas pyarrow fastparquet
```

## Configuration
Replace the API credentials in `main.py`:
```python
API_KEY = "YOUR_API_KEY"
SECRET_KEY = "YOUR_SECRET_KEY"
```

## Usage

### Basic Usage

```python
from datetime import datetime
from assets.main import fetch_multiple_stocks

symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

summary = fetch_multiple_stocks(symbols, start_date, end_date)
```

### Reading Saved Data

```python
# Using CSV
import pandas as pd
df_csv = pd.read_csv('data/processed/AAPL_data.csv')

# Using Parquet
df_parquet = pd.read_parquet('data/processed/AAPL_data.parquet')
```

## Project Structure
```
├── data/
│   ├── raw/           # Raw JSON responses from API
│   └── processed/     # Processed CSV and Parquet files
├── main.py           # Main script
└── README.md         # This file
```

## Understanding Parquet vs CSV

### Why Parquet?

1. **Storage Efficiency**
   - Parquet files are typically 2-4x smaller than CSV
   - Column-based storage enables better compression
   - Example: 1GB CSV file might be 250MB in Parquet

2. **Performance**
   - Faster read times, especially for large datasets
   - Column-based access (great for specific column queries)
   - Optimized for analytical queries

3. **Data Type Preservation**
   - Maintains proper data types (dates stay dates)
   - No type inference needed on each read
   - Consistent schema enforcement

### Performance Comparison Example
```python
# Reading specific columns
# CSV: Reads entire file
df_csv = pd.read_csv('large_file.csv')[['timestamp', 'close']]

# Parquet: Only reads required columns
df_parquet = pd.read_parquet('large_file.parquet', columns=['timestamp', 'close'])
```

### Compatibility
- Fully supported in pandas
- Works seamlessly in Jupyter notebooks
- Supported by most data analysis tools (Spark, Dask, etc.)
- Compatible with cloud storage systems (S3, GCS)

### When to Use Which Format

**Use CSV when:**
- You need human-readable files
- Sharing with non-technical users
- Quick data inspection is needed
- Small datasets (<100MB)

**Use Parquet when:**
- Working with large datasets (>100MB)
- Running frequent analytical queries
- Memory efficiency is important
- Processing data in chunks
- Running distributed computations

## Tips for Working with Parquet

### In Jupyter Notebooks
```python
# Reading Parquet
df = pd.read_parquet('data/processed/AAPL_data.parquet')

# Quick inspection
print(df.info())  # Shows memory usage
print(df.head())  # View first rows

# Reading specific date ranges (faster than CSV)
df_filtered = pd.read_parquet(
    'data/processed/AAPL_data.parquet',
    filters=[('timestamp', '>=', '2023-01-01')]
)
```

### Memory Efficient Reading
```python
# Read specific columns
df = pd.read_parquet(
    'data/processed/AAPL_data.parquet',
    columns=['timestamp', 'close', 'volume']
)

# Read in chunks
for chunk in pd.read_parquet('data/processed/AAPL_data.parquet', chunksize=10000):
    # Process each chunk
    pass
```

## Contributing
Feel free to submit issues and enhancement requests!

## License
MIT License - feel free to use this code for your projects!