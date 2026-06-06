#!/usr/bin/python3
import re

fruits = [
    "apple",
    "banana",
    "orange",
    "bananas"
]

lx = lambda x: re.fullmatch("b.+a", x)
result = list(filter(lx, fruits))

print(result)
