#!/usr/bin/python3
#############################################################################
# Idea from: Deep Dive 2
# Author: Carlos Lacaci Moya
# Description:Iterable vs Iterator
# Date: lun 25 jul 2022 08:31:13 CEST
# Dependencies:
#############################################################################
class Cyties:
    """Iterable class of list of cities
    When iterating over a sequence Python looks first for __iter__ if not found
    looks for __getitem__ and creates an iterator object

    So in a sequence there is no need to implement __iter__
    """
    def __init__(self):
        self.cyties = ["Madrid", "Cadiz", "Granada", "Málaga"]

    def __len__(self):
        return len(self.cyties)

    def __getitem__(self, key: int):
        return self.cyties[key]


class CitiesIter:
    """Iterator class of list of cities"""
    def __init__(self, cyties: Cyties):
        self.idx = 0
        self.cities = cyties

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx >= len(self.cities):
            raise StopIteration
        else:
            result = self.cities[self.idx]
            self.idx += 1
            return result


if __name__ == "__main__":
    cyties = Cyties()
    it = CitiesIter(cyties)
    for i in it:
        print(i)
