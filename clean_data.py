import pandas as pd
import numpy as np
import re

# File paths
RAW_FILE = "data/stock_market_raw.csv"
OUTPUT_FILE = "data/cleaned.parquet"

# Function to convert column names to snake_case
def to_snake(s):
    s = s.strip()
    s = re.sub(r'[\s/]+', '_', s)
    s = re.sub(r'[^A-Za-z0-9_]', '', s)
    return s.lower()

def main():
    print("Loading CSV...")
    df = pd.read_csv(RAW_FILE)

    print("Shape:", df.shape)
    print("Preview:\n", df.head())

    # Normalize column names
    df.columns = [to_snake(c) for c in df.columns]

    # Replace invalid values
    invalid = ["", "NA", "N/A", "null", "Null", "-", " "]
    df = df.replace(invalid, np.nan)

    # Standardize text columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip().str.lower()

    # Parse date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # Remove duplicates
    df = df.drop_duplicates()

    # Save cleaned file
    df.to_parquet(OUTPUT_FILE, index=False)
    print("Saved cleaned file →", OUTPUT_FILE)

if __name__ == "__main__":
    main()

