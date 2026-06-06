# Functions — decorators, closures, partials, memoization, lambdas

## Quick Start
```bash
python 03_decorator.py
python 03_closure.py
python 03_partial.py
python 03_memoization_1.py
python 03_memoization_2.py
python 03_lambdas.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `03_decorator.py` | Function wrapper for timing | `@wraps(orig_func)`, wrapper captures `*args, **kwargs`, `time.perf_counter()` |
| `03_closure.py` | Functions that remember their enclosing scope | `def outer(x): def inner(y): return x+y; return inner` |
| `03_partial.py` | Freeze function arguments with `functools.partial` | `partial(convert_to_base, base=16)`, creates specialized versions |
| `03_memoization_1.py` | Manual cache dict for expensive calls | `cache = {}`, check-then-compute, `time.sleep()` simulates cost |
| `03_memoization_2.py` | LRU cache with doubly-linked list + hash map | `LRUCache(func)`, Node with prev/next, `cache_limit = 3` |
| `03_lambdas.py` | Anonymous functions for filter/map | `lambda x: re.fullmatch("b.+a", x)`, `filter(lx, fruits)` |

## Common Patterns
```python
from functools import wraps, partial, lru_cache
import time

# Decorator — wrap a function with extra behavior
def perf_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"[{func.__name__}] took {time.perf_counter() - t1:.4f}s")
        return result
    return wrapper

# Closure — factory that bakes in state
def make_multiplier(factor):
    def multiply(x):
        return x * factor       # factor is "closed over"
    return multiply

doubler = make_multiplier(2)
doubler(5)  # 10

# Partial — freeze arguments left-to-right
from functools import partial
hex_to_int = partial(int, base=16)
hex_to_int("1A")  # 26

# Memoization — cache results
# Manual:
cache = {}
def memoized(n):
    if n not in cache:
        cache[n] = expensive(n)
    return cache[n]

# Built-in:
@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

# Lambda — tiny anonymous function
sorted(items, key=lambda x: x["age"])       # sort by age
list(filter(lambda x: x > 0, numbers))      # keep positives
```

## Now Build Your Own
Write `function_toolbox.py` that:
1. Creates a `@retry(max_attempts=3, delay=0.5)` decorator — retries a function on `Exception`, sleeping `delay` seconds between attempts.
2. Creates a closure factory `make_counter(start=0)` — returns a function that increments and returns the count each call.
3. Uses `partial` to create `csv_reader = partial(open, mode="r", newline="")` and `json_writer = partial(open, mode="w")`.
4. Implements `@lru_cache` on a recursive function that computes the edit distance (Levenshtein) between two strings.
5. Uses `sorted()` with a lambda to sort a list of dicts by multiple keys.
