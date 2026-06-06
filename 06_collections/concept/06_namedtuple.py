#!/usr/bin/python3
###############################################################################
# Author: Carlos Lacaci Moya
# Description: named_tuple practice
# Date:
# Dependencies:
###############################################################################
"""Ways to create a namedtupple"""
from collections import namedtuple


def custom_divmod(x, y):
    DivMod = namedtuple("DivMod", "quotient remainder")
    #Return values as tuple
    return DivMod(*divmod(x, y))


result = custom_divmod(12, 5)
print(result)
print(result.quotient)
print(result.remainder)

# Default values are assigned to the rightmost argument
# Default value is for phone
Employee = namedtuple("Employee", ["name", "job", "phone"],
                      defaults=["not assigned"])
employee1 = Employee("Carlos Lacaci", "Programmer")
print(employee1)
