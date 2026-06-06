#!/usr/bin/python3
"""
File: demo_multiple_constructors.py
Author: RealPython.com
Email: 
Web: https://realpython.com/python-multiple-constructors/#defining-multiple-class-constructors
Description: Providing multiple constructors
"""
from functools import singledispatchmethod


class DemoClass:

    @singledispatchmethod
    def generic_method(self, arg):
        print(f"Do something with argument of type: {type(arg).__name__}")

    @generic_method.register
    def _(self, arg: int):
        print("Implementation for an int argument...")

    @generic_method.register(str)
    def _(self, arg):
        print("Implementation for a str argument...")


if __name__ == "__main__":
    d1 = DemoClass().generic_method(4.5)
    d2 = DemoClass().generic_method(15)
    d3 = DemoClass().generic_method("carlos")
