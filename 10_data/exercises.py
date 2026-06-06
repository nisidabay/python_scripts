#!/usr/bin/env python3
"""Data exercises: CSV I/O, GroupBy aggregations, NumPy broadcasting, merges, pivot tables."""

import csv
import io
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 1: Load CSV, filter rows, compute mean of a column
# ═══════════════════════════════════════════════════════════════════════════════

csv_data = io.StringIO("""\
name,department,salary
Alice,Engineering,95000
Bob,Marketing,72000
Carlos,Engineering,110000
Diana,Marketing,68000
Eve,Engineering,105000
Frank,Sales,88000
""")
df = pd.read_csv(csv_data)

# Filter only Engineering department, then compute mean salary
eng = df[df["department"] == "Engineering"]
mean_salary = eng["salary"].mean()

print("Exercise 1 — Filter & mean:")
print(df)
print(f"\nEngineering mean salary: ${mean_salary:,.2f}")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 2: GroupBy + multiple aggregations (count, mean, sum)
# ═══════════════════════════════════════════════════════════════════════════════

# Group by department and compute multiple stats in one call
agg = (
    df.groupby("department")["salary"]
    .agg(["count", "mean", "sum"])
    .rename(columns={"count": "employees", "mean": "avg_salary", "sum": "total_payroll"})
)

print("Exercise 2 — GroupBy multiple aggregations:")
print(agg)
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 3: NumPy broadcasting — normalize a 2D array (z-score per column)
# ═══════════════════════════════════════════════════════════════════════════════

# Create a 4x3 array: 4 samples, 3 features (age, height_cm, weight_kg)
data = np.array([
    [25, 175, 70],
    [30, 180, 82],
    [22, 168, 65],
    [35, 185, 90],
], dtype=np.float64)

# Z-score normalization: (x - mean) / std per column
# Broadcasting subtracts row-vector mean from each row, then divides by row-vector std
mean = data.mean(axis=0)   # shape (3,) — row vector
std = data.std(axis=0)     # shape (3,) — row vector
normalized = (data - mean) / std  # broadcasting aligns axes automatically

print("Exercise 3 — NumPy broadcasting normalization:")
print("Original:")
print(data)
print("\nMean per column:", mean)
print("Std per column: ", std)
print("\nNormalized (z-scores):")
print(normalized)
# Verify each column now has mean ≈ 0, std ≈ 1
print("\n  Column means after norm:", normalized.mean(axis=0).round(12))
print("  Column stds after norm: ", normalized.std(axis=0).round(12))
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 4: Merge two DataFrames on a common column
# ═══════════════════════════════════════════════════════════════════════════════

# Department budget table
budgets = pd.DataFrame({
    "department": ["Engineering", "Marketing", "Sales", "HR"],
    "budget": [500_000, 300_000, 400_000, 200_000],
    "headcount_planned": [12, 6, 8, 4],
})

# Inner merge on department — only rows present in BOTH tables survive
merged = df.merge(budgets, on="department", how="inner")

print("Exercise 4 — Inner merge:")
print("Employees:")
print(df)
print("\nBudgets:")
print(budgets)
print("\nMerged (inner):")
print(merged)
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# BONUS: Pivot table with margins
# ═══════════════════════════════════════════════════════════════════════════════

# Create a richer dataset with dates for pivoting
sales_data = pd.DataFrame({
    "region": ["North", "North", "South", "South", "East", "East", "North"],
    "product": ["Widget", "Gadget", "Widget", "Gadget", "Widget", "Gadget", "Gadget"],
    "quarter": ["Q1", "Q2", "Q1", "Q2", "Q1", "Q2", "Q1"],
    "revenue": [1500, 2200, 1800, 1900, 2100, 2400, 1700],
})

# Pivot: region vs product, sum revenue, with margin totals
pivot = pd.pivot_table(
    sales_data,
    values="revenue",
    index="region",
    columns="product",
    aggfunc="sum",
    margins=True,         # add "All" row and column
    margins_name="Total", # label for margins
    fill_value=0,
)

print("BONUS — Pivot table with margins:")
print(sales_data)
print("\nPivot (region × product, sum of revenue):")
print(pivot)
print("---")

print("All data exercises passed.")
