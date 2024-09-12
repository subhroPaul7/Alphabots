import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import datetime
from functools import reduce

def unique(list1):
    ans = reduce(lambda re, x: re+[x] if x not in re else re, list1, [])
    return ans

st.set_page_config(
    page_title="Metaborong x Alphabots",
    page_icon="📈"
)
st.title("Long/Short trade prediction 📈")
df = pd.read_csv("data/data-NSE_FO_35000.csv")
df.columns = df.columns.str.lower()
flag=True
df['date'] = pd.to_datetime(df['date'])
times_list = df['date'].dt.time.astype(str).tolist()
date = df['date'].dt.date.astype(str).tolist()
lst = unique(date)
min_date = datetime.date(2024, 6, 28)
max_date = datetime.date(2024, 8, 30)
test_date = st.date_input("Select a date between 28 June 2024 and 30 August 2024",
    value=min_date,
    min_value=min_date,
    max_value=max_date)
date_str = test_date.strftime("%Y-%m-%d")
pos = lst.index(date_str)
start = pos*375
end = (pos+1)*375
flag=True
if pos == 0:
    close = df[["close"]].iloc[start:end].reset_index(drop=True)
elif pos == 1:
    close = df[["close"]].iloc[start:end-1].reset_index(drop=True)
else:
    close = df[["close"]].iloc[start-1:end-1].reset_index(drop=True)

square_off_price = close["close"][374]
opening = close["close"][0] # time- 9:16
# threshold = st.slider('Select a value for the first threshold', min_value=close['close'].min(), max_value=close['close'].max(), value=opening)
threshold = st.selectbox("Select the time for base price for the trade", times_list[:375])
pos1 = times_list[:375].index(threshold)
base_price = close['close'][pos1]
st.write(f"Base price at selected time: {base_price}")
# Creating the second slider with steps of 2
percentage = st.slider('Select a value for the percentage', min_value=0.00, max_value=10.00, value=0.1, step=0.01)
long_threshold = 1+(percentage/100)
short_threshold = 1-(percentage/100)
no_of_trades = 2
long1 = []
short = []
j=0
for i in close["close"][pos:]:
    if j>=no_of_trades:
        break
    if i>=base_price*long_threshold:
        long1.append(True)
        short.append(False)
        j+=1
    elif i<=base_price*short_threshold:
        long1.append(False)
        short.append(True)
        j+=1
    else:
        long1.append(False)
        short.append(False)
    # opening = i
i1 = 400
i2 = 400
buy1_time = 0
buy2_time = 0
buy1_price = 0
buy2_price = 0
trade1_type = ""
trade2_type = ""
change1 = 0
change2 = 0
profit1 = False
profit2 = False
if True in long1:
    i1 = long1.index(True)
    # st.info(long1[i1:])
    if True in long1[i1+1:]:
        i2 = long1.index(True, long1.index(True)+1)
        buy1_time = times_list[i1+pos1]
        buy2_time = times_list[i2+pos1]
        buy1_price = close["close"][i1+pos1]
        buy2_price = close["close"][i2+pos1]
        change1 = buy1_price - square_off_price
        change2 = buy2_price - square_off_price
        if square_off_price>buy1_price:
            profit1 = True
        if square_off_price>buy2_price:
            profit2 = True
        trade1_type = "long"
        trade2_type = "long"
        st.success(f"Long at {buy1_time} at price Rs. {buy1_price}")
        st.success(f"Long at {buy2_time} at price Rs. {buy2_price}")
    elif True in short:
        i2 = short.index(True)
        if i1<i2:
            buy1_time = times_list[i1+pos1]
            buy2_time = times_list[i2+pos1]
            buy1_price = close["close"][i1+pos1]
            buy2_price = close["close"][i2+pos1]
            change1 = buy1_price - square_off_price
            change2 = square_off_price - buy2_price
            if square_off_price>buy1_price:
                profit1 = True
            if square_off_price<buy2_price:
                profit2 = True
            trade1_type = "long"
            trade2_type = "short"
            st.success(f"Long at {buy1_time} at price Rs. {buy1_price}")
            st.success(f"Short at {buy2_time} at price Rs. {buy2_price}")
        else:
            buy1_time = times_list[i2+pos1]
            buy2_time = times_list[i1+pos1]
            buy1_price = close["close"][i1+pos1]
            buy2_price = close["close"][i2+pos1]
            change1 = square_off_price - buy1_price
            change2 = buy2_price - square_off_price
            if square_off_price<buy1_price:
                profit1 = True
            if square_off_price>buy2_price:
                profit2 = True
            trade1_type = "short"
            trade2_type = "long"
            st.success(f"Short at {buy1_time} at price Rs. {buy1_price}")
            st.success(f"Long at {buy2_time} at price Rs. {buy2_price}")
    else:
        buy1_time = times_list[i1+pos1]
        buy1_price = close['close'][i1+pos1]
        change1 = buy1_price - square_off_price
        if square_off_price>buy1_price:
            profit1 = True
        trade1_type = "long"
        st.success(f"Long at {buy1_time} at price Rs. {buy1_price}")
        st.info("Only 1 trade possible today.")
elif True in short:
    i1 = short.index(True)
    if True in short[i1+1:]:
        i2 = short.index(True, short.index(True)+1)
        buy1_time = times_list[i1+pos1]
        buy2_time = times_list[i2+pos1]
        buy1_price = close["close"][i1+pos1]
        buy2_price = close["close"][i2+pos1]
        change1 = square_off_price - buy1_price
        change2 = square_off_price - buy2_price
        if square_off_price<buy1_price:
            profit1 = True
        if square_off_price<buy2_price:
            profit2 = True
        trade1_type = "short"
        trade2_type = "short"
        st.success(f"Short at {buy1_time} at price Rs. {buy1_price}")
        st.success(f"Short at {buy2_time} at price Rs. {buy2_price}")
    elif True in long1:
        i2 = long1.index(True)
        if i1<i2:
            buy1_time = times_list[i1+pos1]
            buy2_time = times_list[i2+pos1]
            buy1_price = close["close"][i1+pos1]
            buy2_price = close["close"][i2+pos1]
            change1 = square_off_price - buy1_price
            change2 = buy2_price - square_off_price
            if square_off_price<buy1_price:
                profit1 = True
            if square_off_price>buy2_price:
                profit2 = True
            trade1_type = "short"
            trade2_type = "long"
            st.success(f"Short at {buy1_time} at price Rs. {buy1_price}")
            st.success(f"Long at {buy2_time} at price Rs. {buy2_price}")
        else:
            buy1_time = times_list[i2+pos1]
            buy2_time = times_list[i1+pos1]
            buy1_price = close["close"][i1+pos1]
            buy2_price = close["close"][i2+pos1]
            change1 = buy1_price - square_off_price
            change2 = square_off_price - buy2_price
            if square_off_price>buy1_price:
                profit1 = True
            if square_off_price<buy2_price:
                profit2 = True
            trade1_type = "long"
            trade2_type = "short"
            st.success(f"Long at {buy1_time} at price Rs. {buy1_price}")
            st.success(f"Short at {buy2_time} at price Rs. {buy2_price}")
    else:
        buy1_time = times_list[i1+pos1]
        buy1_price = close["close"][i1+pos1]
        change1 = square_off_price - buy1_price
        if square_off_price<buy1_price:
            profit1 = True
        trade1_type = "short"
        st.success(f"Short at {buy1_time} at price Rs. {buy1_price}")
        st.info("Only 1 trade possible today.")
else:
    st.error("No trade possible today.")
    flag = False

if flag==True:
    plt.figure(figsize=(10, 6))
    plt.plot(times_list[:375], close['close'][:375], linestyle='-', color='b')

    if i1!=400:
        plt.scatter(buy1_time,close['close'][i1+pos1], color='red', label='Trade')
    if i2!=400:
        plt.scatter(buy2_time,close['close'][i2+pos1], color='red')
    plt.scatter(times_list[374], close['close'][374], color = "green", label='Square off')
    # Annotate the scatter points
    if i1!=400:
        plt.annotate(f'{close["close"][i1+pos1]:.2f}', (buy1_time, close['close'][i1+pos1]), textcoords="offset points", xytext=(0,10), ha='center', color='black')
    if i2!=400:
        plt.annotate(f'{close["close"][i2+pos1]:.2f}', (buy2_time, close['close'][i2+pos1]), textcoords="offset points", xytext=(0,10), ha='center', color='black')
    plt.annotate(f'{close["close"][374]:.2f}', (times_list[374], close['close'][374]), textcoords="offset points", xytext=(0,10), ha='center', color='green')
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
        if change1!=0:
            if profit1:
                st.info(f"Profit of Rs. {abs(change1)} per share for 1st trade")
            else:
                st.info(f"Loss of Rs. {abs(change1)} per share for 1st trade")
        else:
            st.info(f"Break even for 1st trade")

        if trade2_type!="":
            if change2!=0:
                if profit2: 
                    st.info(f"Profit of Rs. {abs(change2)} per share for 2nd trade")
                else:
                    st.info(f"Loss of Rs. {abs(change2)} per share for 2nd trade")
            else:
                st.info(f"Break even for 2nd trade")

        # net_change = change1 + change2
        # if change2>0:
        #     st.info(f"Net Profit of Rs. {change2} per share for today")
        # elif change2<0:
        #     st.info(f"Net Loss of Rs. {change2} per share for today")
        # else:
        #     st.info(f"Break even for today")