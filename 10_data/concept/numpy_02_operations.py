#!/usr/bin/env python3
# numpy: universal functions (ufuncs), broadcasting, axis parameter, np.where
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

# --- Universal functions (ufuncs): element-wise vectorized operations ---
print(f"a + b:    {a + b}")                    # [11 22 33 44 55]
print(f"a * b:    {a * b}")                    # [10 40 90 160 250]
print(f"a ** 2:   {a ** 2}")                   # [1 4 9 16 25]
print(f"np.sqrt(a): {np.sqrt(a)}")             # [1. 1.414 1.732 2. 2.236]
print(f"np.sin(a):  {np.sin(a)}")
print()

# --- Math ufuncs ---
print(f"np.sum(a):        {np.sum(a)}")         # 15
print(f"np.mean(a):       {np.mean(a):.2f}")    # 3.00
print(f"np.median(a):     {np.median(a)}")      # 3.0
print(f"np.std(a):        {np.std(a):.4f}")     # population std
print(f"np.cumsum(a):     {np.cumsum(a)}")      # [1 3 6 10 15]
print()

# --- Broadcasting: operate on arrays of different shapes ---
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])                  # shape (2, 3)
vec = np.array([10, 100, 1000])                 # shape (3,)  → broadcasted to (2, 3)
print(f"Matrix:\n{matrix}")
print(f"Matrix + vec (broadcast):\n{matrix + vec}")
print()

# Column vector broadcasts across columns
col = np.array([[10], [20]])                    # shape (2, 1) → broadcasted to (2, 3)
print(f"Matrix * col (broadcast):\n{matrix * col}")
print()

# --- axis parameter: operate along rows (0) or columns (1) ---
m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
print(f"Sum axis=0 (columns): {m.sum(axis=0)}")  # [12 15 18]
print(f"Sum axis=1 (rows):    {m.sum(axis=1)}")  # [6 15 24]
print(f"Mean axis=0:          {m.mean(axis=0)}") # [4. 5. 6.]
print()

# --- np.where: vectorized if-else ---
arr = np.array([-5, 3, -2, 8, 0, -1])
# Replace negatives with 0, keep positives
pos = np.where(arr > 0, arr, 0)
print(f"Original: {arr}")
print(f"Positives only: {pos}")                 # [0 3 0 8 0 0]

# Two-value where: positive → 1, else → -1
signs = np.where(arr > 0, 1, -1)
print(f"Signs:          {signs}")               # [-1  1 -1  1 -1 -1]

# where can also return indices for boolean indexing
neg_indices = np.where(arr < 0)
print(f"Negative indices: {neg_indices}")       # (array([0, 2, 5]),)
