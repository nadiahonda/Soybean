import cot_reports as cot
import pandas as pd
from datetime import datetime
import sys
import os

# Adiciona o caminho da raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tvdatafeed_lib.main import TvDatafeed, Interval

def fetch_cot_data(year):
    df = cot.cot_year(year=year, cot_report_type='legacy_fut')
    return df

def process_cot_data(df, commodity):
    filtered_df = df[[
        "Market and Exchange Names", 
        "As of Date in Form YYYY-MM-DD", 
        "Noncommercial Positions-Long (All)", 
        "Noncommercial Positions-Short (All)", 
        "Change in Noncommercial-Long (All)", 
        "Change in Noncommercial-Short (All)",
        "% of OI-Noncommercial-Long (All)",
        "% of OI-Noncommercial-Short (All)"
    ]]
    
    commodity_df = filtered_df[
        filtered_df["Market and Exchange Names"].str.contains(commodity, case=False, na=False) & 
        ~filtered_df["Market and Exchange Names"].str.contains('MINI', case=False, na=False)
    ]
    
    return commodity_df

def calculate_cot(df, cot_type):
    df[f'{cot_type}_COT_%'] = (df["% of OI-Noncommercial-Long (All)"] - df["% of OI-Noncommercial-Short (All)"])
    df = df.rename(columns={'As of Date in Form YYYY-MM-DD': 'datetime'})
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime')
    df = df.sort_values(by='datetime')
    
    return df[[f'{cot_type}_COT_%']]

def extract_COT(start_year=2024):
    current_year = datetime.now().year
    commodities = {
        'ZL': 'SOYBEAN OIL',
        'ZM': 'SOYBEAN MEAL',
        'ZS': 'SOYBEANS'
    }
    
    all_data = {key: [] for key in commodities.keys()}
    
    for year in range(start_year, current_year + 1):
        cot_data = fetch_cot_data(year)
        if cot_data is not None:
            for cot_type, commodity in commodities.items():
                commodity_df = process_cot_data(cot_data, commodity)
                if commodity_df is not None and not commodity_df.empty:
                    all_data[cot_type].append(commodity_df)
                else:
                    print(f"No data found for {commodity} in {year}.")
        else:
            print(f"Error fetching COT data for {year}.")
    
    final_df = pd.DataFrame()
    
    for cot_type, data_list in all_data.items():
        if data_list:
            combined_data = pd.concat(data_list)
            cot_df = calculate_cot(combined_data, cot_type)
            
            if final_df.empty:
                final_df = cot_df
            else:
                final_df = final_df.join(cot_df, how='outer')

    if not final_df.empty:
        return final_df
    else:
        print("No soybean data found for the specified period.")
        raise Exception("No data found")

def update_cot_reports():
    try:
        df_existing = pd.read_parquet('data/cot_soybean_products.parquet')
    except FileNotFoundError:
        df_existing = pd.DataFrame()

    df_new = extract_COT()
    df_combined = pd.concat([df_existing, df_new]).sort_index()
    df_combined = df_combined.drop_duplicates()
    
    df_combined.to_parquet('data/cot_soybean_products.parquet', index=True)
    print("COT data for soybean products saved to 'data/cot_soybean_products.parquet'")

def update_ohlcv_data():
    tv = TvDatafeed()
    
    symbols = {
        'ZS': 'ZS1!',
        'ZL': 'ZL1!',
        'ZM': 'ZM1!'
    }

    for symbol_key, symbol in symbols.items():
        df_new = tv.get_hist(symbol=symbol, exchange='CBOT', interval=Interval.in_daily, n_bars=5000)
        df_new = df_new.drop(['symbol'], axis=1, errors='ignore')

        # try:
        #     df_existing = pd.read_parquet(f'data/{symbol_key}_1D.parquet')
        # except FileNotFoundError:
        #     df_existing = pd.DataFrame()

        # df_combined = pd.concat([df_existing, df_new])
        # df_combined = df_combined.sort_index()
        # df_combined = df_combined.drop_duplicates()

        df_new.to_parquet(f'data/{symbol_key}_1D.parquet', index=True)
        print(f"OHLCV data for {symbol_key} saved to 'data/{symbol_key}_1D.parquet'")

if __name__ == '__main__':
    update_cot_reports()
    update_ohlcv_data()
