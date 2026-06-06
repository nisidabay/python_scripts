#!/usr/bin/env python3
# Standard library power tools you shouldn't reinvent.

from collections import Counter
from itertools import chain, groupby, product
from functools import lru_cache
import statistics
import time

# Counter: frequency table in one line
votes = ["Carlos", "Ana", "Carlos", "Luis", "Ana", "Carlos", "Marta"]
tally = Counter(votes)  # dict subclass with count values
print(f"Winner: {tally.most_common(1)[0]}")  # most_common returns [(elem, count)]
print(f"Carlos votes: {tally['Carlos']}")
tally.update(["Carlos", "Ana"])  # add more votes incrementally

# itertools.chain: flatten iterables without nested loops
a = [1, 2, 3]
b = [4, 5]
chained = list(chain(a, b))  # one flat list, O(1) memory, no intermediate copy
print(f"Chained: {chained}")

# itertools.groupby: cluster consecutive items by key (sort first!)
scores = [("Carlos", 92), ("Ana", 88), ("Carlos", 95), ("Ana", 91)]
scores.sort(key=lambda x: x[0])  # groupby needs sorted input
for name, group in groupby(scores, key=lambda x: x[0]):
    marks = [s for _, s in group]
    print(f"{name}: {marks} (avg {statistics.mean(marks):.1f})")

# itertools.product: Cartesian product — all combinations
roles = ["dev", "reviewer"]
people = ["Carlos", "Ana"]
for role, person in product(roles, people):
    print(f"  {person} as {role}")

# functools.lru_cache: memoize expensive calls automatically
@lru_cache(maxsize=128)  # cache the last 128 calls
def fibonacci(n: int) -> int:
    """Recursive fib — O(2^n) without cache, O(n) with."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

start = time.perf_counter()
result = fibonacci(35)  # 9,227,465 — instant with cache
elapsed = time.perf_counter() - start
print(f"fib(35)={result} in {elapsed*1000:.1f}ms (cached)")
print(f"Cache info: {fibonacci.cache_info()}")

# statistics: mean, median, stdev — no numpy needed for basics
data = [92, 88, 95, 78, 85]
print(f"mean={statistics.mean(data):.1f}, median={statistics.median(data)}, stdev={statistics.stdev(data):.1f}")

if __name__ == "__main__":
    assert tally["Carlos"] == 4, f"Expected 4 after update, got {tally['Carlos']}"
    assert fibonacci(10) == 55
    print("stdlib gems checks passed")
