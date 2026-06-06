#!/usr/bin/python3
"""
File: callable_objects.py
Author: RealPython.com
Email: 
Web: https://realpython.com/python-multiple-constructors/#defining-multiple-class-constructors
Description: Using __call__ to create callable objects

The special method .__call__() turns the instances of CumulativePowerFactory into 
callable objects. In other words, you can call the instances of CumulativePowerFactory 
like you call any regular function.

Inside .__call__(), you first compute the power of base raised to exponent.
Then you add the resulting value to the current value of .total. Finally, you
return the computed power.
"""


class Power:

    def __init__(self, exponent=2, start=0):
        """ Create the power of a number 
        Args:
            exponent: default 2
            start: accumulate calculated power operation
        """
        self._exponent = exponent
        self.total = start

    def __call__(self, base):
        power = base**self._exponent
        self.total += power
        return power


if __name__ == "__main__":
    a = Power()
    print(a(8))
    print(a(9))
    print(f"total is: {a.total}")
