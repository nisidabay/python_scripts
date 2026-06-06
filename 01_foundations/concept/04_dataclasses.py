#!/usr/bin/env python3
# Dataclasses: boilerplate-free value objects with batteries included.

from dataclasses import dataclass, field, asdict, replace
from typing import List
from datetime import datetime

@dataclass(order=True)  # auto-generates __lt__, __le__, __gt__, __ge__
class Person:
    name: str
    age: int
    # default_factory: fresh mutable default per instance (not shared!)
    tags: List[str] = field(default_factory=list)  # avoids mutable-default trap
    created: datetime = field(default_factory=datetime.now)  # timestamp on init

@dataclass(frozen=True)  # immutable — hashable, thread-safe, set/dict-key safe
class Point:
    x: float
    y: float
    label: str = "origin"

# Instantiate — no __init__ to write
carlos = Person(name="Carlos", age=34, tags=["python", "arch"])
ana = Person(name="Ana", age=28)

print(carlos)  # auto __repr__: Person(name='Carlos', age=34, ...)
print(ana)

# Comparison — order=True gives total ordering by field order
print(f"Carlos > Ana by age: {carlos > ana}")  # 34 > 28

# asdict: convert to dict for JSON/serialization
d = asdict(carlos)
print(f"Dict: {d}")

# replace: copy with changes — ergonomic for immutable dataclasses
p1 = Point(3.0, 4.0, "A")
p2 = replace(p1, x=10.0)  # new Point, same y and label
print(f"Original: {p1}, Shifted: {p2}")

# Frozen guard: uncomment to see AttributeError
# p1.x = 99

if __name__ == "__main__":
    assert carlos.age == 34
    assert ana.tags == [], "default_factory should give fresh empty list"
    assert p2.x == 10.0 and p2.y == 4.0, "replace should keep untouched fields"
    print("dataclass checks passed")
