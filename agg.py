import streamlit as st
import pandas as pd

st.set_page_config(page_title="📈 Stock Market Dashboard", layout="wide")

st.title("📊 Stock Market Dashboard")
st.write("Interactive visualization of stock trends and aggregations")

# Load parquet files
agg1 = pd.read_parquet("agg1.parquet")  # has: trade_date, ticker, avg_close
agg2 = pd.read_parquet("agg2.parquet")  # has: ticker, avg_volume
agg3 = pd.read_parquet("agg3.parquet")  # has: ticker, trade_date, daily_return

# Rename date column for consistency
agg1.rename(columns={"trade_date": "date"}, inplace=True)
agg3.rename(columns={"trade_date": "date"}, inplace=True)

# Sidebar filters
tickers = agg1['ticker'].unique().tolist()
selected_tickers = st.sidebar.multiselect(
    "Select Ticker(s)", tickers, default=tickers[:3]
)

# Convert to datetime
agg1['date'] = pd.to_datetime(agg1['date'])
agg3['date'] = pd.to_datetime(agg3['date'])

min_date, max_date = agg1['date'].min(), agg1['date'].max()

selected_dates = st.sidebar.date_input(
    "Select Date Range", [min_date, max_date]
)

# Filter records
mask = (
    (agg1['ticker'].isin(selected_tickers)) &
    (agg1['date'] >= pd.to_datetime(selected_dates[0])) &
    (agg1['date'] <= pd.to_datetime(selected_dates[1]))
)

filtered = agg1[mask]

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily Average Close Price")
    st.line_chart(filtered.set_index('date')[['avg_close']])

with col2:
    st.subheader("Average Volume by Ticker")
    vol_filtered = agg2[agg2['ticker'].isin(selected_tickers)]
    st.bar_chart(vol_filtered.set_index('ticker')['avg_volume'])

st.subheader("Daily Returns")
ret_filtered = agg3[agg3['ticker'].isin(selected_tickers)]
st.line_chart(ret_filtered.set_index('date')[['daily_return']])

st.success("✅ Dashboard loaded successfully!") 