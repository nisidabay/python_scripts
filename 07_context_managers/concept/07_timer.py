#!/usr/bin/env python3
# Context manager: measure execution time using time.perf_counter
import time
from contextlib import contextmanager


class Timer:
    """Context manager that measures elapsed wall-clock time inside a with-block.

    Uses time.perf_counter() for the highest-resolution monotonic clock available.
    """

    def __enter__(self):
        self.start = time.perf_counter()       # snapshot at entry
        return self                            # return self so caller can access .elapsed

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()         # snapshot at exit
        self.elapsed = self.end - self.start   # compute delta
        return False  # don't suppress exceptions


# Alternative: using the @contextmanager decorator (same result, less boilerplate)
@contextmanager
def timer(label="Block"):
    """Generator-based timer with an optional label."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] took {elapsed:.6f} seconds")


if __name__ == "__main__":
    # --- Class-based usage ---
    with Timer() as t:
        total = sum(range(10_000_000))  # simulate work
    print(f"Sum: {total}, elapsed: {t.elapsed:.6f}s")

    # --- Decorator-based usage ---
    with timer("Data crunch"):
        data = [i ** 2 for i in range(5_000_000)]

    # --- Compare two approaches ---
    iterations = 1_000_000
    with Timer() as t1:
        squares = [n * n for n in range(iterations)]

    with Timer() as t2:
        squares_gen = (n * n for n in range(iterations))
        # Force the generator to actually compute
        _ = sum(squares_gen)

    print(f"List comprehension: {t1.elapsed:.4f}s")
    print(f"Generator + sum:    {t2.elapsed:.4f}s")
