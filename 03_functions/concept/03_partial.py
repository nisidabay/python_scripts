#!/usr/sbin/python3
#
# Function for converting numbers to different bases
"""Convert integers numbers to different bases"""

from functools import partial


# Function for converting numbers to different bases
def convert_to_base(_input: str, base: int) -> int:
    """Function for converting numbers to different bases"""
    return int(str(_input), base)


# Create specialized conversion functions
hex_to_int = partial(convert_to_base, base=16)
bin_to_int = partial(convert_to_base, base=2)
oct_to_int = partial(convert_to_base, base=8)

# Usage
print(hex_to_int("1A"))  # Output: 26
print(bin_to_int("1010"))  # Output: 10
print(oct_to_int("777"))  # Output: 511
