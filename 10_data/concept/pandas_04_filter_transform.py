#!/usr/bin/env python3
# pandas: Boolean indexing, .loc, .iloc, .query(), .apply()
import pandas as pd
import numpy as np

# --- Build a DataFrame with varied data ---
np.random.seed(42)
df = pd.DataFrame({
    "name":    ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace"],
    "age":     [25, 30, 35, 28, 22, 40, 33],
    "city":    ["NYC", "LA", "Chicago", "Houston", "Phoenix", "NYC", "LA"],
    "salary":  [70_000, 85_000, 95_000, 72_000, 65_000, 110_000, 88_000],
    "score":   [87.5, 92.0, 78.3, 95.1, 88.0, 74.2, 90.7],
    "dept":    ["Eng", "Mkt", "Eng", "HR", "Mkt", "Eng", "HR"],
})
print(df)
print()

# --- Boolean indexing (mask) ---
high_salary = df[df["salary"] > 80_000]                       # single condition
print("=== Salary > 80k ===")
print(high_salary[["name", "salary"]])
print()

nyc_eng = df[(df["city"] == "NYC") & (df["dept"] == "Eng")]   # compound mask
print("=== NYC AND Engineering ===")
print(nyc_eng)
print()

# --- .query(): SQL-like filtering ---
result = df.query("age >= 30 and score > 80")
print("=== .query('age >= 30 and score > 80') ===")
print(result)
print()

# --- .loc: label-based selection ---
print("=== .loc[2:4, ['name','age','city']] ===")
print(df.loc[2:4, ["name", "age", "city"]])   # rows 2-4 (inclusive), 3 columns
print()

# --- .iloc: integer-position-based selection ---
print("=== .iloc[1:3, 0:3] ===")
print(df.iloc[1:3, 0:3])                      # rows 1-2, columns 0-2
print()

# --- .apply(): apply a function along an axis ---
def salary_band(sal):
    if sal < 75_000:
        return "Low"
    elif sal < 90_000:
        return "Mid"
    else:
        return "High"

df["band"] = df["salary"].apply(salary_band)  # apply to a single column
print("=== Salary bands ===")
print(df[["name", "salary", "band"]])
print()

# --- .apply() with axis=1 (row-wise) ---
df["seniority"] = df.apply(
    lambda row: "Senior" if row["age"] > 30 else "Junior", axis=1
)
print("=== Senior/Junior ===")
print(df[["name", "age", "seniority"]])
print()

# --- .where(): conditional replacement ---
df["score_grade"] = np.where(df["score"] >= 90, "A", "B")
print("=== Score grades ===")
print(df[["name", "score", "score_grade"]])
