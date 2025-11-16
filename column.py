import pandas as pd

df = pd.read_parquet("data/cleaned.parquet")

print("\n--- COLUMN NAMES EXACTLY AS FOUND ---")
print(df.columns.tolist())
