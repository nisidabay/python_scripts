# Data Analysis — Pandas & NumPy fundamentals for data manipulation

## Quick Start
```bash
# Pandas: Series creation, indexing, basic operations
python pandas_01_series.py

# Pandas: DataFrame construction, .info(), .describe(), column/row access
python pandas_02_dataframe.py

# Pandas: read_csv, to_csv, to_json, head/tail, dtypes
python pandas_03_read_write.py

# Pandas: Boolean indexing, .loc/.iloc, .query(), .apply()
python pandas_04_filter_transform.py

# Pandas: .groupby(), .agg(), pivot_table, split-apply-combine
python pandas_05_groupby.py

# NumPy: array creation, dtype, shape, reshape, arange, linspace, slicing
python numpy_01_arrays.py

# NumPy: ufuncs, broadcasting, axis parameter, np.where
python numpy_02_operations.py

# NumPy: Boolean mask indexing, fancy indexing, argmax/argmin
python numpy_03_indexing.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `pandas_01_series.py` | Series from list/dict, custom index, vectorized arithmetic, .str accessor, missing data | `pd.Series([…], index=[…], name=…)`, `.mean()/.max()/.idxmax()`, `.fillna()` |
| `pandas_02_dataframe.py` | DataFrame from dict-of-lists, .info(), .describe(), .iloc/.loc, column operations | `pd.DataFrame(dict)`, `df["col"]`, `df.sort_values()`, `.value_counts()` |
| `pandas_03_read_write.py` | CSV/TSV I/O, .head()/.tail(), .shape, .to_csv(), .to_json(), usecols | `pd.read_csv(buf, sep=…)`, `.to_csv(index=False)`, `.to_json(orient="records")` |
| `pandas_04_filter_transform.py` | Boolean masks, compound conditions, .query(), .loc/.iloc, .apply() axis | `df[(cond1) & (cond2)]`, `.query("age >= 30")`, `.apply(func, axis=1)` |
| `pandas_05_groupby.py` | Split-apply-combine, multi-agg, .transform(), pivot_table, .filter() | `df.groupby("col").agg(total=…, avg=…)`, `.pivot_table(values=, index=, columns=)` |
| `numpy_01_arrays.py` | Array creation, dtype control, .arange/.linspace, .reshape, .random, slicing views | `np.array([…])`, `.reshape(3,4)`, `np.random.seed(42)`, view vs copy |
| `numpy_02_operations.py` | Universal functions, broadcasting, axis sums/means, np.where conditional selection | `a + b` (element-wise), `broadcast (2,3)+(3,)`, `.sum(axis=0)`, `np.where(arr>0,arr,0)` |
| `numpy_03_indexing.py` | Boolean masks, compound masks, in-place mask mutation, fancy indexing, argmax/argmin | `arr[mask]`, `arr[[0,3,5]]`, `np.argmax(arr)`, `np.ix_(rows, cols)` for 2D |

## Common Patterns
```python
import pandas as pd
import numpy as np

# DataFrame from dict, basic inspection
df = pd.DataFrame({"Name": ["A","B"], "Age": [25,30], "Salary": [70_000, 85_000]})
df.info(); df.describe(); df.head(3)

# Boolean filtering + column operations
df["Bonus"] = df["Salary"] * 0.10
high_earners = df[df["Salary"] > 80_000]
result = df.query("Age >= 28 and Salary > 75_000")

# GroupBy with multiple aggregations
df.groupby("dept").agg(
    total=("salary", "sum"),
    avg=("salary", "mean")
)

# Pivot table
df.pivot_table(values="sales", index="region", columns="product", aggfunc="sum")

# NumPy vectorized operations
a = np.arange(10)
a * 2                     # [0 2 4 6 8 ...]
np.where(a > 5, a, 0)     # conditional replacement
a[a % 2 == 0]             # boolean mask indexing
a[[9,8,7]]                # fancy indexing reorder
```

## Now Build Your Own
**Challenge:** Load a CSV of student records (create one with `Name,Math,Science,English,History` and 10+ rows). Calculate each student's average, add an "Average" column, filter to students with average >= 75, group by a "Grade" column (A:>=90, B:80-89, C:70-79, D:<70) and report count and mean scores per grade. Export the summary as JSON.
