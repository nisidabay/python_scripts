#!/usr/bin/env python3
# exercises.py — Group 03: Functions
# 4 solved exercises + BONUS. Run: python3 exercises.py

import functools
import time
from functools import partial, wraps


# ============================================================
# Exercise 1: Write a decorator that logs function calls
#            (name + args)
# ============================================================

def log_calls(func):
    """Decorator: print function name and arguments every call."""
    @wraps(func)  # preserve original name, docstring, etc.
    def wrapper(*args, **kwargs):
        # Format args/kwargs for readability
        arg_str = ", ".join(
            [repr(a) for a in args] +
            [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        print(f"  [LOG] Calling {func.__name__}({arg_str})")
        result = func(*args, **kwargs)
        print(f"  [LOG] {func.__name__} returned {result!r}")
        return result
    return wrapper

@log_calls
def greet(name: str, greeting: str = "Hola") -> str:
    return f"{greeting}, {name}!"

print("Exercise 1:")
r1 = greet("Carlos")
r2 = greet("Ana", greeting="Buenos días")
assert r1 == "Hola, Carlos!"
assert r2 == "Buenos días, Ana!"
print("---")


# ============================================================
# Exercise 2: functools.partial to create preset functions
# ============================================================

def multiply(a: float, b: float) -> float:
    """Generic multiply — partial freezes one argument."""
    return a * b

# Create specialized functions by fixing one argument
double = partial(multiply, 2)        # always multiply by 2
triple = partial(multiply, b=3)      # always multiply by 3 (via keyword)

print("Exercise 2:")
print(f"  double(7) = {double(7)}")            # 2 * 7 = 14
print(f"  triple(7) = {triple(7)}")            # 7 * 3 = 21
print(f"  partial args: {double.args}, keywords: {double.keywords}")
assert double(7) == 14
assert triple(7) == 21
print("---")


# ============================================================
# Exercise 3: Closure that creates a counter with configurable
#            step
# ============================================================

def make_counter(step: int = 1):
    """Factory: returns a counter function that increments by `step`.

    The inner function 'closes over' the `count` and `step` variables —
    they outlive the outer function's call.
    """
    count = 0

    def counter() -> int:
        nonlocal count  # mutate the closed-over variable, not shadow it
        count += step
        return count

    return counter

print("Exercise 3:")
by_2 = make_counter(step=2)
by_5 = make_counter(step=5)

v1 = by_2()   # 2
v2 = by_2()   # 4
v3 = by_5()   # 5  (independent counter!)
v4 = by_2()   # 6

print(f"  by_2: {v1}, {v2}, {v4}  |  by_5: {v3}")
assert (v1, v2, v3, v4) == (2, 4, 5, 6), "Each closure maintains its own state"
print("---")


# ============================================================
# Exercise 4: Chain decorators (timer + logger) on one function
# ============================================================

def timer(func):
    """Decorator: measure and print elapsed time for the call."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [TIMER] {func.__name__} took {elapsed:.6f}s")
        return result
    return wrapper

# Stack decorators: timer wraps logger, logger wraps the function
# Execution order: timer.enter → logger.enter → func → logger.exit → timer.exit

@timer
@log_calls
def compute_squares(n: int) -> list[int]:
    """Compute squares from 0 to n-1 with a tiny delay."""
    time.sleep(0.01)  # simulate real work
    return [i ** 2 for i in range(n)]

print("Exercise 4:")
squares = compute_squares(3)
print(f"  result: {squares}")
assert squares == [0, 1, 4]
# The decorator stack means func.__name__ should be 'compute_squares' (wraps preserves it)
assert compute_squares.__name__ == "compute_squares"
print("---")


# ============================================================
# BONUS: lru_cache benchmark: fibonacci with/without cache
# ============================================================

# Version WITHOUT cache — exponential O(2^n)
def fib_uncached(n: int) -> int:
    if n < 2:
        return n
    return fib_uncached(n - 1) + fib_uncached(n - 2)

# Version WITH lru_cache — linear O(n) after warm-up
@functools.lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

print("BONUS:   lru_cache benchmark")
n = 35
# Only time the cached version; uncached fib(35) takes seconds
start = time.perf_counter()
result_cached = fib_cached(n)
elapsed_cached = time.perf_counter() - start

print(f"  fib_cached({n}) = {result_cached} in {elapsed_cached*1000:.3f} ms")
print(f"  cache info: {fib_cached.cache_info()}")

# Verify both produce the same result (test with a small n)
for i in range(20):
    assert fib_uncached(i) == fib_cached(i), f"Mismatch at fib({i})"
print(f"  ✅ Verified fib(0..19) match for both implementations")

print("---")
print("✅ All Group 03 exercises passed!")
