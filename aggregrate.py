import pandas as pd

def generate_aggregations():
    """Generate summary data (aggregations) from the cleaned stock dataset."""

    # Load the cleaned dataset
    df = pd.read_parquet("data/cleaned.parquet")
    print("Loaded cleaned.parquet:", df.shape)
    print("Columns available:", df.columns.tolist())

    # Column names
    date_col = "trade_date"
    close_col = "close_price"
    volume_col = "volume"

    # Convert to numeric
    df[close_col] = pd.to_numeric(df[close_col], errors="coerce")
    df[volume_col] = pd.to_numeric(df[volume_col], errors="coerce")

    # Drop rows where close_price is missing
    df = df.dropna(subset=[close_col])

    # ---------------------------
    # 1) Daily average close price
    # ---------------------------
    daily_avg_close = (
        df.groupby(['ticker', date_col], as_index=False)
          .agg(avg_close=(close_col, 'mean'))
    )
    daily_avg_close.to_parquet("data/agg1.parquet", index=False)
    print("✅ Saved data/agg1.parquet")

    # ---------------------------
    # 2) Average trading volume
    # ---------------------------
    avg_volume = (
        df.groupby('ticker', as_index=False)
          .agg(avg_volume=(volume_col, 'mean'))
    )
    avg_volume.to_parquet("data/agg2.parquet", index=False)
    print("✅ Saved data/agg2.parquet")

    # ---------------------------
    # 3) Daily returns
    # ---------------------------
    df = df.sort_values(['ticker', date_col])
    df['prev_close'] = df.groupby('ticker')[close_col].shift(1)
    df['daily_return'] = (df[close_col] / df['prev_close']) - 1

    daily_returns = df.dropna(subset=['daily_return'])
    daily_returns.to_parquet("data/agg3.parquet", index=False)
    print("✅ Saved data/agg3.parquet")

if __name__ == "__main__":
    generate_aggregations()
import streamlit as st
import pandas as pd

st.title("Stock Data Aggregations Dashboard")

df = pd.read_parquet("data/cleaned.parquet")
st.write("### Raw Data Preview", df.head())

# Add your aggregations here…

st.success("Aggregations generated successfully!")
