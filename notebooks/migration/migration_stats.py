"""
Purpose: Extract population estimates for Florida and Miami-Dade county 
to establish a baseline of implied migration flows.
Data Sources: 
- FRED Series ID: FLPOP (Resident Population in Florida)
- FRED Series ID: FLMIAM7POP (Resident Population in Miami-Dade County, FL)
"""

import os
import io
import requests
import pandas as pd

def get_fred_data(series_id):
    """Fetch data directly from FRED graph CSV endpoint using robust HTTP requests."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    print(f"Fetching {series_id} from {url} ...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    
    # Read CSV, parse dates, set observation_date as index
    df = pd.read_csv(io.StringIO(response.text), index_col='observation_date', parse_dates=True, na_values=['.'])
    
    # Explicitly handle missing values (NaNs) as required by project rules
    df.ffill(inplace=True)
    df.dropna(inplace=True)
    return df

def main():
    try:
        # Fetch Florida Population (thousands)
        fl_pop = get_fred_data('FLPOP')
        fl_pop.rename(columns={'FLPOP': 'Florida_Pop_Thousands'}, inplace=True)
        
        # Fetch Miami-Dade Population (thousands)
        miami_pop = get_fred_data('FLMIAM6POP')
        miami_pop.rename(columns={'FLMIAM6POP': 'Miami_Dade_Pop_Thousands'}, inplace=True)
        
    except Exception as e:
        print(f"Error fetching migration data: {e}")
        return

    # Merge datasets
    df = pd.merge(fl_pop, miami_pop, left_index=True, right_index=True, how='inner')
    
    # Calculate Year-over-Year implied migration (change in population)
    df['FL_Implied_Net_Migration_Thousands'] = df['Florida_Pop_Thousands'].diff()
    df['Miami_Implied_Net_Migration_Thousands'] = df['Miami_Dade_Pop_Thousands'].diff()
    
    # Drop the first row which will have NaNs from the diff()
    # Explicitly handle missing values (NaNs) before generating visualizations/data files
    df.dropna(inplace=True)
    
    # Convert index name to Year for standardizing
    df.index.name = 'Year'

    # Save to data/migration/ ensuring correct path resolution
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    out_dir = os.path.join(project_root, 'data', 'migration')
    os.makedirs(out_dir, exist_ok=True)

    csv_path = os.path.join(out_dir, 'migration_data.csv')
    df.to_csv(csv_path)
    print(f"Migration data successfully extracted and saved to {csv_path}")

if __name__ == "__main__":
    main()
