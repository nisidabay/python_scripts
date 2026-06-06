#!/usr/bin/env python3
# pandas: .groupby(), .agg(), pivot_table — split-apply-combine
import pandas as pd

# --- Build a sales dataset ---
df = pd.DataFrame({
    "region":   ["East", "West", "East", "West", "East", "West", "East", "West"],
    "product":  ["A", "A", "B", "B", "A", "B", "B", "A"],
    "sales":    [100, 150, 200, 250, 130, 300, 210, 170],
    "quantity": [10, 12, 20, 25, 13, 30, 21, 14],
    "year":     [2023, 2023, 2023, 2023, 2024, 2024, 2024, 2024],
})
print(df)
print()

# --- .groupby(): split by a column, then aggregate ---
# Group by region, sum sales
region_sales = df.groupby("region")["sales"].sum()
print("=== Total sales by region ===")
print(region_sales)
print()

# --- Multiple aggregations with .agg() ---
region_stats = df.groupby("region").agg(
    total_sales=("sales", "sum"),
    avg_sales=("sales", "mean"),
    max_sales=("sales", "max"),
    total_quantity=("quantity", "sum"),
)
print("=== Region stats (multi-agg) ===")
print(region_stats)
print()

# --- Group by multiple columns ---
prod_region = df.groupby(["product", "region"])["sales"].sum()
print("=== Sales by product AND region ===")
print(prod_region)
print()

# --- .groupby() with .transform() — broadcast group stats back to each row ---
df["pct_of_product"] = (
    df.groupby("product")["sales"].transform(lambda x: x / x.sum() * 100)
)
print("=== Each row as % of its product group total ===")
print(df[["product", "region", "sales", "pct_of_product"]].round(1))
print()

# --- pivot_table: reshape and summarise (like Excel pivot) ---
pivot = df.pivot_table(
    values="sales",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0,
)
print("=== Pivot table: region × product, sum of sales ===")
print(pivot)
print()

# --- pivot_table with multiple values and aggfuncs ---
pivot2 = df.pivot_table(
    values=["sales", "quantity"],
    index="year",
    aggfunc={"sales": ["sum", "mean"], "quantity": "sum"},
)
print("=== Pivot: sales (sum/mean) and quantity (sum) by year ===")
print(pivot2)
print()

# --- .filter() on groups ---
# Only keep groups where total sales > 600
filtered = df.groupby("product").filter(lambda g: g["sales"].sum() > 600)
print("=== Products with total sales > 600 ===")
print(filtered)
