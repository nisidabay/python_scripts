#!/usr/bin/env python3
# exercises.py — Group 05: Iterators & Generators
# 4 solved exercises + BONUS. Run: python3 exercises.py

import itertools
import sys
from collections.abc import Iterator


# ============================================================
# Exercise 1: Custom iterator class (__iter__, __next__) for
#            Countdown
# ============================================================

class Countdown:
    """Iterator that counts down from `start` to 1, then stops."""

    def __init__(self, start: int):
        self.current = start

    def __iter__(self) -> "Countdown":
        # Returning self makes the object its own iterator
        return self

    def __next__(self) -> int:
        if self.current < 1:
            raise StopIteration  # signal the for-loop to end
        value = self.current
        self.current -= 1
        return value

print("Exercise 1:")
# For loop drives the iterator protocol: iter() → repeated next() → StopIteration
cd = Countdown(5)
result = list(cd)  # exhausts the iterator
print(f"  Countdown(5) → {result}")
assert result == [5, 4, 3, 2, 1]
# A second attempt returns empty (iterator is exhausted)
assert list(cd) == []
print("---")


# ============================================================
# Exercise 2: Generator function that yields Fibonacci numbers
# ============================================================

def fibonacci(count: int) -> Iterator[int]:
    """Yield the first `count` Fibonacci numbers.

    Generator functions use yield instead of return — state is suspended
    between yields, not destroyed.
    """
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b   # simultaneous swap — no temp variable needed

print("Exercise 2:")
fibs = list(fibonacci(10))
print(f"  First 10 Fibonacci: {fibs}")
assert fibs == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
print("---")


# ============================================================
# Exercise 3: Generator expression vs list comprehension
#            (memory comparison)
# ============================================================

print("Exercise 3:")
n = 10_000_000

# List comprehension — builds the entire list in memory at once
list_comp = [i ** 2 for i in range(n)]
list_mem = sys.getsizeof(list_comp)  # shallow size of the list object itself

# Generator expression — computes values on demand, O(1) memory footprint
gen_expr = (i ** 2 for i in range(n))
gen_mem = sys.getsizeof(gen_expr)
gen_first = next(gen_expr)  # 0² = 0
gen_second = next(gen_expr) # 1² = 1

print(f"  List comprehension: {list_mem:_} bytes (materialized in memory)")
print(f"  Generator expr:     {gen_mem:_} bytes (lazy, one value at a time)")
print(f"  Generator yields:   {gen_first}, {gen_second}, ...")

# Verify both produce the same values
assert list_comp[0] == gen_first == 0
assert list_comp[1] == gen_second == 1

# Clean up the large list
del list_comp
print("---")


# ============================================================
# Exercise 4: yield from to flatten nested lists
# ============================================================

def flatten(nested):
    """Flatten arbitrarily nested iterables using yield from.

    yield from delegates to another generator (or iterable), yielding
    each of its values in turn — no nested for-loops needed.
    """
    for item in nested:
        if isinstance(item, (list, tuple)):
            # yield from recursively flattens the sub-list
            yield from flatten(item)
        else:
            yield item

print("Exercise 4:")
nested_struct = [1, [2, 3, [4, 5]], "Carlos", (6, 7), [[8]]]
flat = list(flatten(nested_struct))
print(f"  Input:  {nested_struct}")
print(f"  Output: {flat}")
assert flat == [1, 2, 3, 4, 5, "Carlos", 6, 7, 8]
print("---")


# ============================================================
# BONUS: Infinite generator with itertools.islice to limit
# ============================================================

def infinite_counter(start: int = 0):
    """Infinite generator — never raises StopIteration on its own."""
    n = start
    while True:
        yield n
        n += 1

def infinite_cycle(items):
    """Infinite generator — endlessly cycle through a sequence."""
    while True:
        for item in items:
            yield item

print("BONUS:   Infinite generator + islice")

# itertools.islice: slice an iterator like a list, but lazily
counter = infinite_counter(100)
first_ten = list(itertools.islice(counter, 10))
print(f"  islice(counter, 10):       {first_ten}")
assert first_ten == [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]

# islice with start/stop/step
next_five = list(itertools.islice(counter, 5))
print(f"  next 5 (continued):        {next_five}")
# counter resumed from where it left off!
assert next_five == [110, 111, 112, 113, 114]

# Cycle + islice: infinite repeating pattern, limited by islice
colors = infinite_cycle(["rojo", "verde", "azul"])
limited = list(itertools.islice(colors, 8))
print(f"  islice(cycle(colors), 8):  {limited}")
assert limited == ["rojo", "verde", "azul", "rojo", "verde", "azul", "rojo", "verde"]

print("---")
print("✅ All Group 05 exercises passed!")
