# circle.py
"""
File: circle.py
Author: RealPython.com
Email: 
Web: https://realpython.com/python-multiple-constructors/#defining-multiple-class-constructors
Description: Using clasmethod as constructors

Using @classmethod makes it possible to add as many explicit constructors as you
need to a given class. It’s a Pythonic and popular way to implement multiple 
constructors. You can also call this type of constructor an alternative constructor 
in Python

The classmethod returns the instance variable that __init__() needs to create the
object
"""

import math


class Circle:
    """ Create a circle """

    def __init__(self, radius):
        self.radius = radius

    @classmethod
    def from_diameter(cls, diameter):
        """ Create a circle from the diameter """

        return cls(radius=diameter // 2)

    def area(self):
        return math.pi * self.radius**2

    def perimeter(self):
        return 2 * math.pi * self.radius

    def __repr__(self):
        return f"{self.__class__.__name__}(radius={self.radius})"


if __name__ == "__main__":
    c = Circle(25)
    print(c)
    print(c.area())
    print(c.perimeter())

    print()

    d = Circle.from_diameter(50)
    print(d)
    print(d.area())
    print(d.perimeter())
