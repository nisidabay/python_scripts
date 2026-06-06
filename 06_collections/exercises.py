#!/usr/bin/env python3
# exercises.py — Group 06: Collections
# 4 solved exercises + BONUS. Run: python3 exercises.py

import math
from collections import Counter, defaultdict, namedtuple, ChainMap, deque


# ============================================================
# Exercise 1: Counter for word frequency in a text
# ============================================================

print("Exercise 1:")
# Text from Gabriel García Márquez
text = (
    "Muchos años después, frente al pelotón de fusilamiento, el coronel "
    "Aureliano Buendía había de recordar aquella tarde remota en que su padre "
    "lo llevó a conocer el hielo. Macondo era entonces una aldea de veinte "
    "casas de barro y cañabrava construidas a la orilla de un río de aguas "
    "diáfanas que se precipitaban por un lecho de piedras pulidas, blancas y "
    "enormes como huevos prehistóricos."
)

# Counter: dict subclass that maps items → counts
words = text.lower().replace(",", "").replace(".", "").split()
freq = Counter(words)

print(f"  Total words: {len(words)}")
print(f"  Top 5 words: {freq.most_common(5)}")
print(f"  'de' appears: {freq['de']} times")
assert freq["de"] == 7
assert freq.most_common(1)[0][0] == "de"  # most frequent word
print("---")


# ============================================================
# Exercise 2: defaultdict for grouping items by category
# ============================================================

print("Exercise 2:")
# Carlos's team — group employees by department
employees = [
    ("Carlos", "Engineering"),
    ("Ana", "Design"),
    ("Luis", "Engineering"),
    ("Marta", "Design"),
    ("Elena", "Engineering"),
    ("Pedro", "Marketing"),
]

# defaultdict(list): missing key → new empty list (no KeyError)
by_dept = defaultdict(list)
for name, dept in employees:
    by_dept[dept].append(name)

for dept, members in by_dept.items():
    print(f"  {dept}: {', '.join(members)}")

assert by_dept["Engineering"] == ["Carlos", "Luis", "Elena"]
assert len(by_dept["Design"]) == 2
# Accessing a non-existent key creates it automatically (the factory is called)
assert "HR" not in by_dept
_ = by_dept["HR"]  # triggers the default_factory
assert by_dept["HR"] == []  # now it exists with an empty list
print("---")


# ============================================================
# Exercise 3: namedtuple for representing a Point with
#            distance method
# ============================================================

# namedtuple: lightweight, immutable data container with named fields
Point = namedtuple("Point", ["x", "y"])

def distance(p1: Point, p2: Point) -> float:
    """Euclidean distance between two Points."""
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

print("Exercise 3:")
origin = Point(0, 0)
p1 = Point(3, 4)
p2 = Point(10, 2)

print(f"  Points: {origin}, {p1}, {p2}")
print(f"  distance(origin, {p1}) = {distance(origin, p1)}")
print(f"  distance({p1}, {p2}) = {distance(p1, p2):.4f}")

assert distance(origin, p1) == 5.0  # 3-4-5 triangle
assert p1.x == 3 and p1.y == 4
# namedtuples are immutable
try:
    p1.x = 99
except AttributeError as e:
    print(f"  Immutable as expected: {e}")
# But you can _replace (returns a new instance)
p1_shifted = p1._replace(x=99)
print(f"  p1._replace(x=99) → {p1_shifted} (original unchanged: {p1})")
assert p1_shifted.x == 99 and p1.x == 3
print("---")


# ============================================================
# Exercise 4: ChainMap for layered config
#            (defaults → env → CLI)
# ============================================================

print("Exercise 4:")
# ChainMap: search through multiple dicts in order; first match wins
# Perfect for layered configuration: CLI overrides env, env overrides defaults

import os

defaults = {"host": "localhost", "port": 5432, "debug": False}
env_overrides = {}  # filled from environment
# Simulate environment variables
if True:  # simulate ENV being set
    env_overrides["host"] = "db.staging.example.com"
    env_overrides["port"] = 3306
cli_overrides = {"debug": True}  # --debug flag passed on CLI

# ChainMap: later arguments have HIGHER priority (CLI > env > defaults)
config = ChainMap(cli_overrides, env_overrides, defaults)

print(f"  host:  {config['host']}   (from env, overriding default)")
print(f"  port:  {config['port']}   (from env)")
print(f"  debug: {config['debug']}  (from CLI)")
print(f"  All keys visible: {list(config.keys())}")

assert config["host"] == "db.staging.example.com"  # env wins
assert config["port"] == 3306                        # env wins
assert config["debug"] is True                        # CLI wins

# ChainMap.maps exposes the underlying list of mappings
print(f"  maps: {config.maps}")
assert len(config.maps) == 3
print("---")


# ============================================================
# BONUS: deque as a fixed-size sliding window
# ============================================================

print("BONUS:   deque sliding window")

# deque: double-ended queue, O(1) append/pop from both ends
# maxlen=N: automatically drops the oldest item when full

# Rolling average of temperature readings from Carlos's weather station
readings = [22.1, 22.5, 23.0, 22.8, 23.2, 23.5, 24.0, 23.8]

window = deque(maxlen=3)  # sliding window of last 3 readings
averages: list[float] = []

for temp in readings:
    window.append(temp)
    if len(window) == 3:
        avg = sum(window) / len(window)
        averages.append(round(avg, 2))
    print(f"    Reading: {temp:4.1f}  Window: {list(window)}")

print(f"  Moving averages (window=3): {averages}")
assert len(averages) == 6  # 8 readings, window=3 → 6 averages
assert averages[0] == round((22.1 + 22.5 + 23.0) / 3, 2)

# deque also supports appendleft/popleft for FIFO queues
dq = deque(["Carlos", "Ana", "Luis"])
dq.appendleft("Marta")          # add to front
right = dq.pop()                 # remove from back → "Luis"
left = dq.popleft()              # remove from front → "Marta"
print(f"  FIFO operations: {list(dq)}")
assert list(dq) == ["Carlos", "Ana"]

print("---")
print("✅ All Group 06 exercises passed!")
