#!/usr/bin/python3


#############################################################################
# Idea from: Python3 Deep Dive2 - Iterator protocol
# Author: Carlos Lacaci Moya
# Description: Create an Iterable class
# Date: mié 13 jul 2022 12:22:19 CEST
# Dependencies:
#############################################################################
class Squares:

    def __init__(self, length: int):
        self.i = 0
        self.length = length

    def __len__(self):
        return self.length

    def __next__(self):
        if self.i >= self.length:
            raise StopIteration
        else:
            result = self.i**2
            self.i += 1
            return result

    def __iter__(self):
        return self


if __name__ == "__main__":
    sq = Squares(10)
    for i in sq:
        print(i)
