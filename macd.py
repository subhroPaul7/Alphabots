import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
from io import BytesIO

st.set_page_config(
    page_title="Metaborong x Alphabots",
    page_icon="📈"
)
st.title("Long/Short trade prediction 📈")

# Function to calculate MACD and Signal Line
def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    df['EMA_short'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA_long'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
    return df

# Function to generate buy/sell signals based on MACD crossover
def generate_signals(df):
    df['Signal'] = 0
    df['Signal'] = np.where(df['MACD'] > df['Signal_Line'], 1, -1)
    df['Position'] = df['Signal'].diff()

    buy_signals = df[df['Position'] == 2]
    sell_signals = df[df['Position'] == -2]

    return buy_signals, sell_signals

# Function to plot MACD, Signal Line, and MACD Histogram
def plot_macd(df, buy_signals, sell_signals):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['MACD'], label='MACD', color='b', alpha=0.75)
    plt.plot(df.index, df['Signal_Line'], label='Signal Line', color='orange', alpha=0.75)
    # Normalize the histogram values for better visualization
    hist_values = df['MACD_Histogram'].values
    
    # Define colors based on whether the histogram value is positive or negative
    colors = ['green' if val >= 0 else 'red' for val in hist_values]
    
    # Plot the MACD histogram with colors and ensure bars reflect actual values
    plt.bar(df.index, hist_values, color=colors, alpha=0.5, width=0.005)
    
    if not buy_signals.empty:
        plt.plot(buy_signals.index, buy_signals['MACD'], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    if not sell_signals.empty:
        plt.plot(sell_signals.index, sell_signals['MACD'], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
    
    plt.title('MACD Analysis')
    plt.xlabel('Date')
    plt.xticks(rotation=90)
    
    # Convert times to datetime with a consistent date
    start_time = pd.Timestamp("2024-01-01 09:15:00+05:30")
    end_time = pd.Timestamp("2024-01-01 15:30:00+05:30")
    
    # Apply xlim with these datetime objects
    plt.xlim([start_time, end_time])
    
    plt.ylabel('MACD')
    plt.legend(loc='upper left')
    plt.grid(True)
    st.pyplot(plt)

# Read data
df = pd.read_csv("data/TCS_minute_macd.csv")
# Ensure column names are correctly named and cleaned
df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces
df['date'] = pd.to_datetime(df['date'])  # Automatically infer the datetime format
df1 = df[['date', 'Open', 'High', 'Low', 'Close']]
df2 = df[['date', 'Open', 'Close']]
df1 = df1.iloc[:375]
df2 = df2.iloc[:375]
df1.set_index('date', inplace=True)
df2.set_index('date', inplace=True)

# Perform MACD analysis
df_macd = calculate_macd(df2)
# Generate buy and sell signals
buy_signals, sell_signals = generate_signals(df_macd)

def plot_candlestick(df):
    # Create a BytesIO buffer to save the plot
    buf = BytesIO()
    
    # Plot using mplfinance
    mpf.plot(df, type='candle', style='charles', title='Candlestick Chart', xlabel="Time", ylabel='Price', savefig=buf)
    
    # Move the cursor to the start of the BytesIO buffer
    buf.seek(0)
    
    return buf

buf = plot_candlestick(df1)

# Display the plot
st.image(buf)
st.header("All Entry and Exit points")
plot_macd(df_macd, buy_signals, sell_signals)

# Define time range slider
min_time = df2.index.min().time()
max_time = df2.index.max().time()

selected_start_time = st.slider("Select Start Time", min_value=min_time, max_value=max_time, value=min_time)
selected_end_time = st.slider("Select End Time", min_value=min_time, max_value=max_time, value=max_time)

# Filter data based on selected time range
filtered_df = df_macd[df_macd.index.time >= selected_start_time]
filtered_df = filtered_df[filtered_df.index.time <= selected_end_time]

# Generate buy and sell signals for the filtered data
filtered_buy_signals, filtered_sell_signals = generate_signals(filtered_df)

# Combine buy and sell signals and sort by index (date)
all_signals = pd.concat([filtered_buy_signals, filtered_sell_signals]).sort_index()
# Select the first two trades (buy followed by sell or short sell followed by buy)
trades = []
for i in range(len(all_signals) - 1):
    if all_signals['Position'].iloc[i] == 2 and all_signals['Position'].iloc[i + 1] == -2:
        trades.append((all_signals.iloc[i:i+1], all_signals.iloc[i+1:i+2]))
    elif all_signals['Position'].iloc[i] == -2 and all_signals['Position'].iloc[i + 1] == 2:
        trades.append((all_signals.iloc[i+1:i+2], all_signals.iloc[i:i+1]))
    if len(trades) == 2:
        break

c = 1
# Plot MACD, Signal Line, and selected trades
for trade in trades:
    st.header(f"Trade {c}:")
    plot_macd(filtered_df, trade[0], trade[1])
    c += 1

# Calculate and display profit/loss for each trade
for idx, (entry, exit) in enumerate(trades):
    entry_price = entry['Close'].values[0]
    exit_price = exit['Close'].values[0]
    profit_loss = exit_price - entry_price if entry['Position'].values[0] == 2 else entry_price - exit_price

    if entry.index.time<=exit.index.time:
        st.header(f"Trade {idx + 1}: Long")
        st.warning(f"Entry at {entry.index[0]}: {entry_price}")
        st.warning(f"Exit at {exit.index[0]}: {exit_price}")
    else:
        st.header(f"Trade {idx + 1}: Short")
        st.warning(f"Short at {exit.index[0]}: {exit_price}")
        st.warning(f"Buy back at {entry.index[0]}: {entry_price}")   
    if profit_loss<0.00:
        st.error(f"Loss from the trade: {profit_loss:.2f}")
    elif profit_loss>0.00:
        st.success(f"Profit from the trade: {profit_loss:.2f}")
    else:
        st.info("No profit or loss from trade")
# Print buy and sell signals
# st.header("Selected Trades Signals:")
# for idx, (entry, exit) in enumerate(trades):
#     st.write(f"Trade {idx + 1} Entry Signal:")
#     st.write(entry[['Close', 'MACD', 'Signal_Line']])
#     st.write(f"Trade {idx + 1} Exit Signal:")
#     st.write(exit[['Close', 'MACD', 'Signal_Line']])

# Print buy and sell signals
st.header("Buy Signals:")
st.write(filtered_buy_signals[['Close', 'MACD', 'Signal_Line']])

st.header("Sell Signals:")
st.write(filtered_sell_signals[['Close', 'MACD', 'Signal_Line']])
