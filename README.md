# Metaborong x Alphabots 📈

This repository contains two Streamlit applications for analyzing and visualizing trading data. The primary focus is on predicting trade opportunities using technical indicators and visualizing trade signals on candlestick charts.

## Overview

1. **`app.py`**:
   - This Streamlit app allows users to select thresholds and percentage values to determine potential long or short trades.
   - It visualizes the trade signals on a line chart of closing prices and annotates buy/sell points.
   - Trades are determined based on price thresholds set by the user, and only two trades per day are considered.

2. **`macd.py`**:
   - This Streamlit app performs MACD (Moving Average Convergence Divergence) analysis on minute-level stock data.
   - It calculates MACD, Signal Line, and MACD Histogram, and generates buy/sell signals based on MACD crossovers.
   - The app displays candlestick charts and MACD plots with buy/sell signals, and provides a detailed trade analysis.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/repositoryname.git
   cd repositoryname
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Create a `requirements.txt` file with the following content:
   ```
   pandas
   streamlit
   matplotlib
   mplfinance
   numpy
   ```

3. **Prepare your data**:
   - Ensure you have the following CSV files:
     - `data/PAYTM_minute.csv` (for `app.py`)
     - `TCS_minute.csv` (for `macd.py`)

4. **Run the Streamlit apps**:
   - For `app.py`:
     ```bash
     streamlit run app.py
     ```
   - For `macd.py`:
     ```bash
     streamlit run macd.py
     ```

## Features

### `app.py`
- Allows the user to set thresholds and percentage values to identify long/short trade opportunities.
- Displays closing prices with annotated trade signals.
- Provides an interactive visualization of potential trades and trade outcomes.

### `macd.py`
- Calculates and visualizes MACD, Signal Line, and MACD Histogram.
- Displays buy and sell signals based on MACD crossovers.
- Shows candlestick charts and detailed trade analysis.

## Data

- The data used in these apps should be in minute-level format with columns for date and price values. Make sure the CSV files are formatted correctly and located in the appropriate directories.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



