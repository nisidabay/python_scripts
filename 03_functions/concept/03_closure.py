#!/usr/bin/python3
from typing import Callable, Optional

"""Use of closures

closures in Python are a powerful mechanism that allows functions to
"remember" the context in which they were created, enabling advanced programming
techniques like encapsulation, factory functions, callbacks, and more.
"""


def get_number(number) -> Callable:
    def operation(math: str) -> Optional[int]:
        if math == "add":
            return number + number
        elif math == "multiply":
            return number * number

    return operation


def outer_function(x) -> Callable:
    def inner_function(y) -> int:
        return x + y

    return inner_function


if __name__ == "__main__":
    number = get_number(3)
    result = number("add")
    print(result)
    result = number("multiply")
    print(result)

    closure = outer_function(10)
    result = closure(5)
    print(result)
