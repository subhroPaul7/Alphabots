import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys

st.set_page_config(
    page_title="Metaborong x Alphabots",
    page_icon="📈"
)
st.title("Long/Short trade prediction 📈")
df = pd.read_csv("data/TCS_minute.csv")
flag=True
df['date'] = pd.to_datetime(df['date'])
times_list = df['date'].dt.time.astype(str).tolist()
close_2023_01_02 = df[["close"]].iloc[:375]
square_off_price = close_2023_01_02["close"][374]
opening = close_2023_01_02["close"][0] # time- 9:16
threshold = st.slider('Select a value for the first threshold', min_value=close_2023_01_02['close'].min(), max_value=close_2023_01_02['close'].max(), value=opening)

# Creating the second slider with steps of 2
percentage = st.slider('Select a value for the percentage', min_value=0.00, max_value=10.00, value=0.5, step=0.01)
long_threshold = 1+(percentage/100)
short_threshold = 1-(percentage/100)
no_of_trades = 2
long = []
short = []
j=0
for i in close_2023_01_02["close"]:
    if j>=no_of_trades:
        break
    if i>=opening*long_threshold:
        long.append(True)
        short.append(False)
        j+=1
    elif i<=opening*short_threshold:
        long.append(False)
        short.append(True)
        j+=1
    else:
        long.append(False)
        short.append(False)
    # opening = i
buy1_time = 0
buy2_time = 0
buy1_price = 0
buy2_price = 0
trade1_type = ""
trade2_type = ""
change1 = 0
change2 = 0
if True in long:
    i1 = long.index(True)
    st.info(long[i1:])
    if True in long[i1+1:]:
        i2 = long.index(True, long.index(True)+1)
        buy1_time = times_list[i1]
        buy2_time = times_list[i2]
        buy1_price = close_2023_01_02["close"][i1]
        buy2_price = close_2023_01_02["close"][i2]
        change1 = buy1_price - square_off_price
        change2 = buy2_price - square_off_price
        trade1_type = "long"
        trade2_type = "long"
        st.success(f"Long at {buy1_time} at price Rs. {buy1_price}")
        st.success(f"Long at {buy2_time} at price Rs. {buy2_price}")
    elif True in short:
        i2 = short.index(True)
        if i1<i2:
            buy1_time = times_list[i1]
            buy2_time = times_list[i2]
            buy1_price = close_2023_01_02["close"][i1]
            buy2_price = close_2023_01_02["close"][i2]
            change1 = buy1_price - square_off_price
            change2 = square_off_price - buy2_price
            trade1_type = "long"
            trade2_type = "short"
            st.success(f"Long at {buy1_time} at price Rs. {buy1_price}")
            st.success(f"Short at {buy2_time} at price Rs. {buy2_price}")
        else:
            buy1_time = times_list[i2]
            buy2_time = times_list[i1]
            buy1_price = close_2023_01_02["close"][i1]
            buy2_price = close_2023_01_02["close"][i2]
            change1 = square_off_price - buy1_price
            change2 = buy2_price - square_off_price
            trade1_type = "short"
            trade2_type = "long"
            st.success(f"Short at {buy1_time} at price Rs. {buy1_price}")
            st.success(f"Long at {buy2_time} at price Rs. {buy2_price}")
    else:
        buy1_time = times_list[i1]
        buy1_price = close_2023_01_02['close'][i1]
        change1 = buy1_price - square_off_price
        trade1_type = "long"
        st.success(f"Long at {buy1_time} at price Rs. {buy1_price}")
        st.info("Only 1 trade possible today.")
elif True in short:
    i1 = short.index(True)
    if True in short[i1+1:]:
        i2 = short.index(True, short.index(True)+1)
        buy1_time = times_list[i1]
        buy2_time = times_list[i2]
        buy1_price = close_2023_01_02["close"][i1]
        buy2_price = close_2023_01_02["close"][i2]
        change1 = square_off_price - buy1_price
        change2 = square_off_price - buy2_price
        trade1_type = "short"
        trade2_type = "short"
        st.success(f"Short at {buy1_time} at price Rs. {buy1_price}")
        st.success(f"Short at {buy2_time} at price Rs. {buy2_price}")
    elif True in long:
        i2 = long.index(True)
        if i1<i2:
            buy1_time = times_list[i1]
            buy2_time = times_list[i2]
            buy1_price = close_2023_01_02["close"][i1]
            buy2_price = close_2023_01_02["close"][i2]
            change1 = square_off_price - buy1_price
            change2 = buy2_price - square_off_price
            trade1_type = "short"
            trade2_type = "long"
            st.success(f"Short at {buy1_time} at price Rs. {buy1_price}")
            st.success(f"Long at {buy2_time} at price Rs. {buy2_price}")
        else:
            buy1_time = times_list[i2]
            buy2_time = times_list[i1]
            buy1_price = close_2023_01_02["close"][i1]
            buy2_price = close_2023_01_02["close"][i2]
            change1 = buy1_price - square_off_price
            change2 = square_off_price - buy2_price
            trade1_type = "long"
            trade2_type = "short"
            st.success(f"Long at {buy1_time} at price Rs. {buy1_price}")
            st.success(f"Short at {buy2_time} at price Rs. {buy2_price}")
    else:
        buy1_time = times_list[i1]
        buy1_price = close_2023_01_02["close"][i1]
        change1 = square_off_price - buy1_price
        trade1_type = "short"
        st.success(f"Short at {buy1_time} at price Rs. {buy1_price}")
        st.info("Only 1 trade possible today.")
else:
    st.error("No trade possible today.")
    flag = False

if flag==True:
    plt.figure(figsize=(10, 6))
    plt.plot(times_list[:375], df['close'][:375], linestyle='-', color='b')

    plt.scatter(buy1_time,close_2023_01_02['close'][i1], color='red', label='Trade')
    plt.scatter(buy2_time,close_2023_01_02['close'][i2], color='red')
    plt.scatter(times_list[374], df['close'][374], color = "green", label='Square off')
    # Annotate the scatter points
    plt.annotate(f'{df["close"][i1]:.2f}', (buy1_time, df['close'][i1]), textcoords="offset points", xytext=(0,10), ha='center', color='black')
    plt.annotate(f'{df["close"][i2]:.2f}', (buy2_time, df['close'][i2]), textcoords="offset points", xytext=(0,10), ha='center', color='black')
    plt.annotate(f'{df["close"][374]:.2f}', (times_list[374], df['close'][374]), textcoords="offset points", xytext=(0,10), ha='center', color='green')
    # Optionally, reduce the number of x-ticks
    plt.xticks(range(0, len(times_list[:375]), 15), rotation=45)

    plt.title('Closing Prices Over Time')
    plt.xlabel('Time')
    plt.ylabel('Close Price')
    plt.grid(True)

    # Rotate date labels for better readability
    plt.xticks(rotation=90)
    plt.legend()
    st.pyplot(plt)

    if trade1_type!="":
        if change1>0:
            st.info(f"Profit of Rs. {change1} per share for 1st trade")
        elif change1<0:
            st.info(f"Loss of Rs. {change1} per share for 1st trade")
        else:
            st.info(f"Break even for 1st trade")

        if trade2_type!="":
            if change2>0:
                st.info(f"Profit of Rs. {change2} per share for 2nd trade")
            elif change2<0:
                st.info(f"Loss of Rs. {change2} per share for 2nd trade")
            else:
                st.info(f"Break even for 2nd trade")

        net_change = change1 + change2
        if change2>0:
            st.info(f"Net Profit of Rs. {change2} per share for today")
        elif change2<0:
            st.info(f"Net Loss of Rs. {change2} per share for today")
        else:
            st.info(f"Break even for today")