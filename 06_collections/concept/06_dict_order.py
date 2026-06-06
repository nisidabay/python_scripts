#!/usr/bin/env python3
# Python 3.7+ dicts preserve insertion order, but OrderedDict has extra methods
from collections import OrderedDict

d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])

# Regular dicts: order ignored for equality (Python 3.7+)
assert d1 == d2                    # same keys/values → equal
assert list(d1) == ["a", "b"]      # insertion order preserved
assert list(d2) == ["b", "a"]      # different insertion order

# OrderedDict: order matters for equality
assert od1 != od2                  # different order → not equal
assert list(od1) == ["a", "b"]

# OrderedDict extras: move_to_end, popitem(last=...)
od1.move_to_end("a")               # move 'a' to the end
assert list(od1) == ["b", "a"]
od1.move_to_end("b", last=False)   # move 'b' to the beginning
assert list(od1) == ["b", "a"]

# popitem(last=False) pops the first item (FIFO)
first = od1.popitem(last=False)
assert first == ("b", 2)
assert list(od1) == ["a"]

print("dict order ✓")
print("OrderedDict extras: move_to_end, popitem(False)")
