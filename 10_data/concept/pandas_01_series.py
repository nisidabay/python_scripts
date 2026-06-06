#!/usr/bin/env python3
# pandas: pd.Series from list/dict, index, .dtype, basic operations
import pandas as pd

# --- Create Series from a list ---
temps_f = pd.Series([32, 45, 60, 72, 85, 98], name="Temperature_F")
print(temps_f)
# 0    32
# 1    45
# 2    60
# 3    72
# 4    85
# 5    98
# Name: Temperature_F, dtype: int64

# --- Custom index ---
cities = pd.Series([32, 45, 60, 72, 85, 98],
                   index=["NYC", "LA", "Chicago", "Houston", "Phoenix", "Miami"],
                   name="Temp_F")
print(cities)
print()

# --- Series from a dict (keys become index) ---
city_pop = pd.Series({
    "NYC": 8_336_000,
    "LA": 3_822_000,
    "Chicago": 2_665_000,
    "Houston": 2_302_000,
}, name="Population")
print(city_pop)
print(f"dtype: {city_pop.dtype}")  # dtype: int64
print()

# --- .dtype and type conversions ---
print(f"Original dtype: {temps_f.dtype}")                   # int64
temps_c = (temps_f - 32) * 5 / 9                            # vectorized arithmetic
print(f"After arithmetic dtype: {temps_c.dtype}")            # float64
print(temps_c.round(1))
print()

# --- Basic operations ---
print(f"Mean temp:    {cities.mean():.1f}°F")
print(f"Max temp:     {cities.max()}°F  (city: {cities.idxmax()})")
print(f"Min temp:     {cities.min()}°F  (city: {cities.idxmin()})")
print(f"Std dev:      {cities.std():.2f}")
print()

# --- Boolean filtering ---
hot = cities[cities > 75]
print("Hot cities (>75°F):")
print(hot)
print()

# --- Element-wise string ops (auto .str accessor when dtype is object) ---
names = pd.Series(["alice", "bob", "charlie", "diana"], name="Name")
print(names.str.upper())        # uppercase
print(names.str.contains("a"))  # boolean mask
print()

# --- Missing data ---
s = pd.Series([1.0, None, 3.5, None, 5.0])
print(f"Has NaN? {s.isna().any()}, count: {s.isna().sum()}")
print(f"Fill NaNs with 0: {s.fillna(0).tolist()}")
