#!/usr/bin/python3
""" Decorator for timing async coroutines """
import functools
from time import perf_counter
from typing import Callable, Any


def async_timed() -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f"Starting [{func.__name__}] with {args} {kwargs}")
            start = perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                print(
                    f"Finished [{func.__name__}] in {perf_counter()-start:.4f} second(s)"
                )

        return wrapped

    return wrapper
