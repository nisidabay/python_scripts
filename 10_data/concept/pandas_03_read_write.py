#!/usr/bin/env python3
# pandas: pd.read_csv, .to_csv, .to_json, .head(), .tail()
import pandas as pd
import io

# --- Create a sample CSV in memory to demonstrate read/write ---
csv_data = """name,age,city,salary
Alice,25,NYC,70000
Bob,30,LA,85000
Charlie,35,Chicago,95000
Diana,28,Houston,72000
Eve,22,Phoenix,65000
Frank,40,NYC,110000
Grace,33,LA,88000
"""

# --- pd.read_csv: read from a file-like object ---
df = pd.read_csv(io.StringIO(csv_data))
print("=== .head(3) ===")
print(df.head(3))                         # first 3 rows
print()

print("=== .tail(2) ===")
print(df.tail(2))                         # last 2 rows
print()

# --- .shape, .columns, .index ---
print(f"Shape: {df.shape}")               # (7, 4)
print(f"Columns: {df.columns.tolist()}")
print(f"Index: {df.index.tolist()}")
print()

# --- .to_csv: write DataFrame to CSV string ---
csv_out = df.to_csv(index=False)
print("=== CSV Output (first 200 chars) ===")
print(csv_out[:200])
print()

# --- .to_json: serialize to JSON ---
json_out = df.to_json(orient="records", indent=2)
print("=== JSON Output (first 300 chars) ===")
print(json_out[:300])
print()

# --- Read with options ---
# Simulate a CSV with different delimiter and header
tsv_data = "city\tpopulation\tstate\nNYC\t8336000\tNY\nLA\t3822000\tCA\n"
df_tsv = pd.read_csv(io.StringIO(tsv_data), sep="\t")
print("=== TSV with tab separator ===")
print(df_tsv)
print()

# --- Read only specific columns ---
df_subset = pd.read_csv(io.StringIO(csv_data), usecols=["name", "age"])
print("=== Subset of columns ===")
print(df_subset)
print()

# --- .dtypes ---
print("=== dtypes ===")
print(df.dtypes)
