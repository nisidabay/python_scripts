#!/usr/sbin/python3
#
# Example of using UserString

"""Example of using UserString"""
from collections import UserString


class MaskCreditCard(UserString):
    """Mask credit card numbers"""

    def __str__(self):
        """Show only last 4 characters, mask the rest"""
        # self.data is given by UserString
        return "*" * (len(self.data) - 4) + self.data[-4:]

    def original(self):
        """Method to get original string"""
        return self.data


# Using the custom string
card = MaskCreditCard("1234567890123456")
print(str(card))
print(card.original())
