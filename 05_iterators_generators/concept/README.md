# Iterators & Generators — iterator protocol, generators, lazy evaluation, yield from

## Quick Start
```bash
python 05_iterator_class.py
python 05_iterators_and_iterables.py
python 05_generator_usage.py
python 05_lazy_evaluation.py
python 05_factor.py
python 05_iterating_over_sequence-1.py
python 05_iterating_over_sequence-2.py
python 05_iterating_over_sequence-3.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `05_iterator_class.py` | Full iterator protocol (`__iter__` + `__next__`) | `class Squares:` with `self.i`, `StopIteration`, `__iter__` returns `self` |
| `05_iterators_and_iterables.py` | Separating collection from iterator | `Cities` (iterable with `__getitem__`), `CityIterator` (iterator with `__next__`) |
| `05_generator_usage.py` | Generator function with `yield` for infinite sequences | `def transaction_id(tid): while True: tid+=1; yield tid` |
| `05_lazy_evaluation.py` | Compute only when accessed via `@property` | `self._area = None`, property checks-then-computes, invalidates on setter |
| `05_factor.py` | Generator for mathematical sequences | `yield k`, `yield n // k`, while `k**2 <= n` |
| `05_iterating_over_sequence-1.py` | Iterable via `__getitem__`, separate iterator class | `Numbers` (no `__iter__`, just `__getitem__`), `Squares` as iterator |
| `05_iterating_over_sequence-2.py` | Iterable + separate iterator for lists | `Cyties` with `__getitem__`, `CitiesIter` with `__next__` |
| `05_iterating_over_sequence-3.py` | Generic iterator over any `Sequence[str]` | `CitiesIter` takes `Sequence[str]`, works with plain lists too |

## Common Patterns
```python
from typing import Iterator, Sequence

# Iterator class — full protocol
class Squares:
    def __init__(self, length):
        self.i = 0
        self.length = length

    def __iter__(self):
        return self                          # an iterator returns itself

    def __next__(self):
        if self.i >= self.length:
            raise StopIteration
        result = self.i ** 2
        self.i += 1
        return result

# Iterable (collection) + separate Iterator
class Cities:
    def __init__(self):
        self._cities = ["Paris", "Berlin", "Rome"]
    def __len__(self):
        return len(self._cities)
    def __getitem__(self, pos):
        return self._cities[pos]            # Python auto-creates iterator

class CityIterator:
    def __init__(self, cities):
        self._cities = cities
        self._index = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index >= len(self._cities):
            raise StopIteration
        item = self._cities[self._index]
        self._index += 1
        return item

# Generator function — simplest way to make an iterator
def factor_generator(n: int) -> Iterator[int]:
    k = 1
    while k * k <= n:
        if n % k == 0:
            yield k                          # pauses here, resumes on next()
            yield n // k
        k += 1

# Infinite generator
def counter(start=0):
    while True:
        yield start
        start += 1

# Lazy evaluation with property
class Circle:
    def __init__(self, r):
        self.radius = r                      # calls setter
        self._area = None

    @property
    def area(self):
        if self._area is None:               # compute only once
            self._area = math.pi * self.radius ** 2
        return self._area

    @radius.setter
    def radius(self, r):
        self._radius = r
        self._area = None                    # invalidate cache
```

## Now Build Your Own
Write `range_toolkit.py` with:
1. An iterator class `RangeIterator` that mimics `range(start, stop, step)` — implement `__iter__` and `__next__`.
2. A generator function `fibonacci(n)` that yields the first `n` Fibonacci numbers.
3. A generator function `chunked(iterable, size)` that yields chunks (lists) of `size` elements (e.g., `chunked("ABCDEFG", 3)` → `['A','B','C']`, `['D','E','F']`, `['G']`).
4. A class `LazyDataset` that loads a large file lazily: only reads lines when iterated, never loads the whole file into memory.
5. A generator `flatten(nested)` that recursively yields all non-list elements from an arbitrarily nested list using `yield from`.
