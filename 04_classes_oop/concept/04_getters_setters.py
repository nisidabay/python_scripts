#!/usr/bin/python3
###############################################################################
# Author: Carlos Lacaci Moya
# Description: Usage of getters and setters
# Date:
# Dependencies:
###############################################################################
class Age:
    def __init__(self, age):
        """ Calling the property """
        self.age = age

    @property
    def age(self):
        """ Retrives the value """
        print("Getting value")
        return self._age

    @age.setter
    def age(self, age):
        """ Sets the value """
        print("Setting value")
        self._age = self.check_age(age)

    @staticmethod
    def check_age(age):
        """ Check for valid input type """
        if isinstance(age, int):
            return age
        else:
            raise ValueError("Enter a number")


if __name__ == "__main__":
    a = Age(56)
    print(a.age)
    b = Age(78)
    print(b.age)
