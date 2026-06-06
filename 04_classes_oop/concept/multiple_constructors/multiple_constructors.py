#!/usr/bin/python3
"""
File: multiple_constructors.py
Author: RealPython.com
Email: yourname@email.com
Web: https://realpython.com/python-multiple-constructors/#defining-multiple-class-constructors
Description: Create multiple constructors with singledispatchmethod
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
    a = DemoClass()
    a.generic_method(5)

    b = DemoClass()
    b.generic_method([1, 2, 3])

    c = DemoClass()
    c.generic_method("Hello")
