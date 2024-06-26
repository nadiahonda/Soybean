# Soybean Data Analysis

This project is a Streamlit application for analyzing continuous soybean contract data (ZS, ZL, ZM). It allows for data updates and interactive chart visualizations.

## Project Structure

- **data/**: Contains the parquet files with OHLCV data.
- **scripts/**: Contains scripts for data updating and extraction.
- **app/**: Contains the main components of the Streamlit application.
- **tvdatafeed_lib/**: Contains a copy of the TvDataFeed library, which is currently offline.
- **requirements.txt**: Project dependency list.
- **README.md**: Project documentation.

## How to Run

1. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

## Features

- OHLCV data and COT reports updating.
- Interactive chart visualization with Plotly and Lightweight Charts
- Time range filter via a sidebar slider.
