#!/usr/bin/python3

#############################################################################
# Idea from: Python3 Deep Dive2 - Lazy Evaluation
# Author: Carlos Lacaci Moya
# Description: Only calculate area when needed
# Date: mié 13 jul 2022 21:47:53 CEST
# Dependencies:
#############################################################################
import math


class Circle:

    def __init__(self, r):

        # Call the property
        self.radius = r
        self._area = None

    @property
    def radius(self):
        print("calling getter property")
        return self._radius

    @radius.setter
    def radius(self, r):
        print("calling setter property")
        self._radius = r
        self._area = None

    @property
    def area(self):
        if self._area is None:
            print("Calculating area...")
            self._area = math.pi * (self.radius**2)
        return self._area

    def __repr__(self):
        return  f"Circle({self.radius}) area {self._area}"

if __name__ == "__main__":
    c = Circle(2)
    c.area
    print(c)
