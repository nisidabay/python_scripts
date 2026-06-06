#!/usr/bin/python3
#############################################################################
# Idea from: Deep Dive 2
# Author: Carlos Lacaci Moya
# Description:Iterable vs Iterator
# Date: lun 25 jul 2022 08:31:13 CEST
# Dependencies:
#############################################################################
class Numbers:
    """Iterable class of list of numbers

    When iterating over a sequence Python looks first for __iter__ if not found
    looks for __getitem__ and create and iterator object

    So in a sequence there is no need to implement __iter__
    """
    def __init__(self):
        self.numbers = [1, 2, 3, 4, 5]

    def __len__(self):
        return len(self.numbers)

    def __getitem__(self, key):
        return self.numbers[key]


class Squares:
    """Iterator class of squares of list of numbers"""
    def __init__(self, numbers: Numbers):
        self.idx = 0
        self.numbers = numbers

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx >= len(self.numbers):
            raise StopIteration
        else:
            result = self.numbers[self.idx]**2
            self.idx += 1
            return result


if __name__ == "__main__":
    numbers = Numbers()
    sq = Squares(numbers)
    for i in sq:
        print(i)
