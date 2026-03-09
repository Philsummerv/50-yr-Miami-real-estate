"""
Miami-Dade Housing vs. Gold Price Analysis

Purpose: 
To fetch historical Miami-Dade Housing Price Index (HPI) and Gold prices, 
calculate the ratio of HPI to ounces of gold, and visualize the trend 
from 1976 onwards.

Data Sources:
1. Miami-Dade HPI: FRED API (Series ID: ATNHPIUS12086A)
2. Gold Prices: datahub.io (raw GitHub dataset: gold-prices)
"""

import os
import pandas as pd
import datetime
import plotly.express as px
import yfinance as yf

def get_fred_data(series_id):
    """Fetch data directly from FRED graph CSV endpoint."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    print(f"Fetching {series_id} from {url} ...")
    # Read CSV, parse dates, set observation_date as index, and coercion on bad data
    df = pd.read_csv(url, index_col='observation_date', parse_dates=True, na_values=['.'], storage_options={'User-Agent': 'Mozilla/5.0'})
    df.dropna(inplace=True)
    return df

def get_gold_data():
    """Fetch Gold Futures data from public raw Github dataset (datahub.io)"""
    url = "https://raw.githubusercontent.com/datasets/gold-prices/master/data/monthly.csv"
    print(f"Fetching Gold data from {url}...")
    df = pd.read_csv(url, parse_dates=['Date'])
    
    # Standardize column naming to match our previous logic
    df.rename(columns={'Date': 'observation_date', 'Price': 'Gold_USD'}, inplace=True)
    df.set_index('observation_date', inplace=True)
    df.dropna(inplace=True)
    return df

def main():
    try:
        # ATNHPIUS12086A is the FRED ID for Miami-Dade HPI
        miami_hpi = get_fred_data('ATNHPIUS12086A')
        miami_hpi.rename(columns={'ATNHPIUS12086A': 'Miami_HPI'}, inplace=True)
        
        # Get Gold from yfinance
        gold_price = get_gold_data()
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        import traceback
        traceback.print_exc()
        return

    # Filter from 1976 onwards
    start_date = pd.to_datetime('1976-01-01')
    miami_hpi = miami_hpi[miami_hpi.index >= start_date]
    gold_price = gold_price[gold_price.index >= start_date]

    print("Aligning and calculating ratio...")
    # Resample to Annual Start (YS) and take mean
    miami_hpi_annual = miami_hpi.resample('YS').mean()
    gold_annual = gold_price.resample('YS').mean()

    # Merge dataframes
    df = pd.merge(miami_hpi_annual, gold_annual, left_index=True, right_index=True, how='inner')
    
    # Calculate Ratio (HPI Index points per ounce of gold)
    df['HPI_in_Gold'] = df['Miami_HPI'] / df['Gold_USD']
    df.index.name = 'Year'

    # Ensure data/gold directory exists
    out_dir = os.path.join('data', 'gold')
    os.makedirs(out_dir, exist_ok=True)

    # Save to CSV
    csv_path = os.path.join(out_dir, 'miami_housing_vs_gold_1976_2026.csv')
    df.to_csv(csv_path)
    print(f"Saved CSV to {csv_path}")

    # Generate Plot
    fig = px.line(
        df.reset_index(), 
        x='Year', 
        y='HPI_in_Gold', 
        title='Miami Real Estate Price Index Priced in Gold (1976-2026)',
        labels={'HPI_in_Gold': 'HPI / Gold Price (Ounces)'}
    )
    png_path = os.path.join(out_dir, 'miami_housing_vs_gold_1976_2026.png')
    fig.write_image(png_path)
    print(f"Saved PNG to {png_path}")

    html_path = os.path.join(out_dir, 'miami_housing_vs_gold_1976_2026.html')
    fig.write_html(html_path)
    print(f"Saved interactive HTML to {html_path}")

    print("Analysis complete! Head over to data/gold to see the results.")

if __name__ == "__main__":
    main()
