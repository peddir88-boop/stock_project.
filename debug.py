import pandas as pd

print("\n--- agg1.parquet ---")
try:
    a1 = pd.read_parquet("agg1.parquet")
    print(a1.head())
    print("Rows:", len(a1))
except Exception as e:
    print(e)

print("\n--- agg2.parquet ---")
try:
    a2 = pd.read_parquet("agg2.parquet")
    print(a2.head())
    print("Rows:", len(a2))
except Exception as e:
    print(e)

print("\n--- agg3.parquet ---")
try:
    a3 = pd.read_parquet("agg3.parquet")
    print(a3.head())
    print("Rows:", len(a3))
except Exception as e:
    print(e) 