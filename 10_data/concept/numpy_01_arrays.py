#!/usr/bin/env python3
# numpy: np.array, dtype, .shape, .reshape, .arange, .linspace
import numpy as np

# --- Create arrays from Python lists ---
a = np.array([1, 2, 3, 4, 5])                 # 1-D array (vector)
b = np.array([[1, 2, 3], [4, 5, 6]])          # 2-D array (matrix)

print(f"a: {a}")
print(f"b:\n{b}")
print(f"a.ndim: {a.ndim}, a.shape: {a.shape}, a.dtype: {a.dtype}")
print(f"b.ndim: {b.ndim}, b.shape: {b.shape}, b.dtype: {b.dtype}")
print()

# --- Specify dtype ---
f_arr = np.array([1, 2, 3], dtype=np.float64)
print(f"f_arr dtype: {f_arr.dtype}")          # float64
c_arr = np.array([1+2j, 3+4j])               # complex inferred automatically
print(f"c_arr dtype: {c_arr.dtype}")          # complex128
print()

# --- .arange: evenly spaced values (start, stop, step) ---
r = np.arange(0, 10, 2)                       # [0 2 4 6 8]
print(f"arange(0, 10, 2): {r}")
print()

# --- .linspace: evenly spaced N values between start and stop (inclusive) ---
ls = np.linspace(0, 1, 5)                     # [0.  0.25 0.5  0.75 1. ]
print(f"linspace(0, 1, 5): {ls}")
print()

# --- .reshape: change shape without copying data ---
flat = np.arange(12)                           # [0..11]
matrix = flat.reshape(3, 4)                    # 3 rows, 4 cols
print(f"Original (1-D): {flat}")
print(f"Reshaped (3x4):\n{matrix}")
print(f"Reshape to (2, 2, 3):\n{flat.reshape(2, 2, 3)}")  # 3-D tensor
print()

# --- .zeros, .ones, .eye, .full ---
print(f"zeros(3):    {np.zeros(3)}")
print(f"ones(2,3):\n{np.ones((2, 3))}")
print(f"eye(3):\n{np.eye(3)}")                # identity matrix
print(f"full((2,3), 7):\n{np.full((2, 3), 7)}")
print()

# --- .random ---
np.random.seed(42)
print(f"rand(3):        {np.random.rand(3)}")          # uniform [0,1)
print(f"randn(2,3):\n{np.random.randn(2, 3)}")         # standard normal
print(f"randint(1, 100, 6): {np.random.randint(1, 100, 6)}")  # integers
print()

# --- Slicing (views, not copies!) ---
arr = np.arange(10)
sub = arr[2:5]
sub[0] = 99                                      # modifies original!
print(f"arr after slice mutation: {arr}")        # [ 0  1 99  3  4  5  6  7  8  9]

# Use .copy() to avoid this
arr2 = np.arange(10)
sub2 = arr2[2:5].copy()
sub2[0] = 99
print(f"arr2 unchanged: {arr2}")                 # [0 1 2 3 4 5 6 7 8 9]
