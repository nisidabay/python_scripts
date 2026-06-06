#!/usr/bin/env python3
# Pythonic idioms every developer should reach for first.

from pathlib import Path
import sys

names = ["Carlos", "Ana", "Carlos", "Luis"]  # real names with a duplicate
ages = {"Carlos": 34, "Ana": 28, "Luis": 41}

# List comprehension with dedup — set comprehension for uniqueness
unique = [n for n in names if n.startswith("C")]  # filter in one line
unique_set = {n for n in names}  # set comprehension: dedup + hash table

# Dict comprehension — transform keys/values in one expression
name_lengths = {n: len(n) for n in unique_set}  # why loop when you can map?

# Unpacking: * grabs leftovers, ** merges dicts
first, *rest = names  # *rest catches everything after first
merged = {**ages, "Marta": 31}  # ** unpacks dict into new dict literal

# f-strings: inline expressions, padding, formatting
for name, age in merged.items():
    print(f"{name:>8} is {age:02d} years old")  # >8 right-align, 02d zero-pad

# enumerate: index + value in one iterator
for i, name in enumerate(names, start=1):  # start=1 for human numbering
    print(f"  {i}. {name}")

# zip: pair iterables side by side
scores = [92, 88, 95]
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

# Walrus operator := — assign and test in one expression
if (n := len(names)) > 3:  # compute once, use in condition AND body
    print(f"Got {n} names — enough for a team")

# __name__ guard: only run when executed, not when imported
if __name__ == "__main__":
    assert len(merged) == 4, "Expected 4 people in merged dict"
    assert rest == ["Ana", "Carlos", "Luis"], "Unpacking rest mismatch"
    print("All idiom checks passed")
