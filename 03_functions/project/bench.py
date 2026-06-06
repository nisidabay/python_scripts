#!/usr/bin/env python3
"""Benchmark decorator tool: CLI that runs Python expressions with timer, cache stats, comparison.

Uses decorators, lru_cache, closures, functools — stdlib only.
"""

from __future__ import annotations

import argparse
import functools
import sys
import time
from typing import Any, Callable, Dict, List, Tuple


# ---------------------------------------------------------------------------
# Benchmark decorator (closure-based)
# ---------------------------------------------------------------------------
def make_benchmark_decorator(iterations: int = 10000):
    """Closure-based decorator factory: returns a decorator tuned to a given iteration count."""

    def benchmark(func: Callable) -> Callable:
        name = func.__name__

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Warm-up
            for _ in range(max(1, iterations // 100)):
                func(*args, **kwargs)

            start = time.perf_counter()
            for _ in range(iterations):
                result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start

            per_call = (elapsed / iterations) * 1_000_000
            print(f"[{name}] {iterations} calls: {elapsed:.4f}s total, {per_call:.2f} µs/call")
            return result

        return wrapper

    return benchmark


# ---------------------------------------------------------------------------
# LRU Cache wrapper
# ---------------------------------------------------------------------------
def cached(func: Callable) -> Callable:
    """Apply functools.lru_cache with cache-info reporting."""
    cached_func = functools.lru_cache(maxsize=128)(func)

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = cached_func(*args, **kwargs)
        info = cached_func.cache_info()
        print(f"[cache] hits={info.hits}, misses={info.misses}, currsize={info.currsize}, maxsize={info.maxsize}")
        return result

    wrapper.cache_info = cached_func.cache_info  # type: ignore[attr-defined]
    wrapper.cache_clear = cached_func.cache_clear  # type: ignore[attr-defined]
    return wrapper


# ---------------------------------------------------------------------------
# Expression runner
# ---------------------------------------------------------------------------
def _make_eval_func(code: Any, scope: Dict[str, Any], use_cache: bool) -> Callable[[], Any]:
    """Create an eval callable, optionally wrapped with lru_cache."""
    import math
    scope["math"] = math

    if use_cache:
        @cached
        def cached_eval() -> Any:
            return eval(code, scope, {})
        return cached_eval
    else:
        def plain_eval() -> Any:
            return eval(code, scope, {})
        return plain_eval


def run_expr(expr: str, iterations: int, use_cache: bool) -> Tuple[float, Any]:
    """Compile and time a simple Python expression."""
    code = compile(expr, "<bench>", "eval")
    scope: Dict[str, Any] = {}
    fn = _make_eval_func(code, scope, use_cache)

    # Warm-up
    for _ in range(max(1, iterations // 100)):
        fn()

    result: Any = None
    start = time.perf_counter()
    for _ in range(iterations):
        result = fn()
    elapsed = time.perf_counter() - start

    per_call = (elapsed / iterations) * 1_000_000
    print(f"Expression: {expr!r}")
    print(f"  {iterations} iterations: {elapsed:.6f}s total, {per_call:.2f} µs/call")
    if use_cache and hasattr(fn, "cache_info"):
        info = fn.cache_info()  # type: ignore[attr-defined]
        print(f"  cache — hits={info.hits}, misses={info.misses}")

    return elapsed, result


# ---------------------------------------------------------------------------
# Decorated example functions (used via `--example`)
# ---------------------------------------------------------------------------

@make_benchmark_decorator(iterations=10000)
def fib(n: int) -> int:
    """Naive fibonacci."""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


@cached
@make_benchmark_decorator(iterations=100)
def fib_cached(n: int) -> int:
    """Cached fibonacci."""
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Benchmark Python expressions with decorators, caching, and comparisons."
    )
    p.add_argument("expr", nargs="?", help="Python expression to benchmark (e.g. 'sum(range(1000))')")
    p.add_argument("-n", "--iterations", type=int, default=10000, help="Number of iterations (default: 10000)")
    p.add_argument("--cache", action="store_true", help="Apply lru_cache to the expression")
    p.add_argument("--example", action="store_true", help="Run built-in fib / fib_cached comparison")
    p.add_argument("--compare", type=str, nargs=2, metavar=("EXPR1", "EXPR2"),
                   help="Compare two expressions")
    return p


def main() -> None:
    args = build_parser().parse_args()

    if args.example:
        print("=== Example: fib(20) naive vs cached ===\n")
        fib_cached.cache_clear()  # type: ignore[attr-defined]
        t1, _ = run_expr("fib(20)", iterations=1, use_cache=False)
        t2, _ = run_expr("fib_cached(20)", iterations=100, use_cache=True)
        print(f"\nResult: {t1 / 1:.2f} s (naive) vs {t2 / 100 * 1e6:.2f} µs/call (cached)")
        return

    if args.compare:
        expr1, expr2 = args.compare
        print(f"=== Comparing: {expr1!r} vs {expr2!r} ({args.iterations} iterations) ===\n")
        t1, r1 = run_expr(expr1, args.iterations, args.cache)
        t2, r2 = run_expr(expr2, args.iterations, args.cache)
        faster = "first" if t1 < t2 else "second"
        ratio = max(t1, t2) / min(t1, t2) if min(t1, t2) > 0 else float("inf")
        print(f"\nWinner: {faster} ({ratio:.2f}x faster)")
        print(f"  Result1: {r1!r}")
        print(f"  Result2: {r2!r}")
        return

    if args.expr:
        run_expr(args.expr, args.iterations, args.cache)
        return

    print("No expression provided. Use --help for usage.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
