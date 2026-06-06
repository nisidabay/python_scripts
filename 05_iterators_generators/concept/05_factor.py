#!/usr/bin/python3
#
# Generate factors of a number
from typing import Iterator


def factor_generator(n) -> Iterator[int]:
    k = 1
    while k**2 <= n:  # Loop until k reaches the square root of n
        if n % k == 0:
            yield k
            yield n // k
        k += 1


# Example usage:
number = 16
factors = list(factor_generator(number))
print("Factors of", number, ":", factors)
