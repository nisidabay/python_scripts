#!/usr/bin/env python3
# numpy: Boolean mask indexing, fancy indexing, np.argmax/argmin
import numpy as np

np.random.seed(42)
scores = np.random.randint(50, 100, size=10)   # 10 random scores 50-99
print(f"Scores: {scores}")
print()

# --- Boolean mask indexing ---
mask = scores >= 80
print(f"Mask (>=80): {mask}")                  # [True, False, ...]
print(f"Top scores:  {scores[mask]}")          # only values where mask is True
print(f"Count >=80:  {mask.sum()}")            # True = 1, sum counts True values
print()

# Compound mask with & (element-wise AND)
mid_mask = (scores >= 65) & (scores < 85)
print(f"Mid scores (65-84): {scores[mid_mask]}")
print()

# --- Modify in-place with boolean mask ---
scores_copy = scores.copy()
scores_copy[scores_copy < 60] = 60             # floor: minimum score is 60
print(f"Floored at 60: {scores_copy}")
print()

# --- Fancy indexing: use integer arrays to select elements ---
indices = [0, 3, 5, 7]                         # pick specific positions
print(f"Fancy index [{indices}]: {scores[indices]}")
print()

# Reorder, repeat, or omit elements arbitrarily
reorder = [9, 8, 7, 6, 5]                      # reverse last 5
print(f"Reordered: {scores[reorder]}")
print()

# --- 2-D fancy indexing ---
matrix = np.arange(1, 17).reshape(4, 4)
print(f"Matrix 4x4:\n{matrix}")
# Select specific rows and columns
rows = [0, 3]                                  # first and last row
cols = [1, 2]                                  # second and third column
print(f"Rows {rows}, cols {cols}:\n{matrix[np.ix_(rows, cols)]}")
print()

# --- np.argmax / np.argmin: index of max/min ---
print(f"argmax (position of max): {np.argmax(scores)}")
print(f"  -> value at that position: {scores[np.argmax(scores)]}")
print(f"argmin (position of min): {np.argmin(scores)}")
print(f"  -> value at that position: {scores[np.argmin(scores)]}")
print()

# argmax/argmin with axis for 2-D
m = np.array([[5, 2, 8],
              [1, 9, 4],
              [7, 3, 6]])
print(f"Matrix:\n{m}")
print(f"argmax axis=0 (max per column): {np.argmax(m, axis=0)}")  # [2, 1, 0]
print(f"argmax axis=1 (max per row):    {np.argmax(m, axis=1)}")  # [2, 1, 0]
print()

# --- Conditional selection: np.extract ---
# np.extract is like boolean mask but returns 1D
evens = np.extract(scores % 2 == 0, scores)
print(f"Even scores: {evens}")
