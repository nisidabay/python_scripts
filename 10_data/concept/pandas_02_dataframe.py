#!/usr/bin/env python3
# pandas: pd.DataFrame from dict, .info(), .describe(), column access
import pandas as pd

# --- DataFrame from a dict-of-lists ---
data = {
    "Name":     ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Age":      [25, 30, 35, 28, 22],
    "City":     ["NYC", "LA", "Chicago", "Houston", "Phoenix"],
    "Salary":   [70_000, 85_000, 95_000, 72_000, 65_000],
    "Dept":     ["Engineering", "Marketing", "Engineering", "HR", "Marketing"],
}
df = pd.DataFrame(data)
print(df)
print()

# --- .info(): schema, dtypes, non-null count, memory ---
print("=== .info() ===")
df.info()
print()

# --- .describe(): summary statistics for numeric columns ---
print("=== .describe() ===")
print(df.describe())
print()

# --- Column access styles ---
print("=== Column Access ===")
print(df["Name"])           # dot notation Series
print(df.Age.tolist())      # attribute access
print(df[["Name", "Age"]])  # multiple columns (returns DataFrame)
print()

# --- Row access ---
print("=== Row Access ===")
print(df.iloc[2])            # 3rd row by integer position
print(df.loc[1])             # row with index label 1
print()

# --- Adding and dropping columns ---
df["Bonus"] = df["Salary"] * 0.10                    # new column from vectorized op
df["Total"] = df["Salary"] + df["Bonus"]
print(df[["Name", "Salary", "Bonus", "Total"]])
print()

# --- Value counts ---
print("=== Department Counts ===")
print(df["Dept"].value_counts())
print()

# --- Sort ---
print("=== Sorted by Age (descending) ===")
print(df.sort_values("Age", ascending=False)[["Name", "Age", "Dept"]])
