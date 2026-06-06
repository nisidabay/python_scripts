#!/usr/bin/python3

#############################################################################
# Idea from: Python3 Deep Dive2 - Separating the Collection from the iterator
# Author: Carlos Lacaci Moya
# Description: Create an Iterable class
# Date: mié 13 jul 2022 12:22:19 CEST
# Dependencies:
#############################################################################

from typing import Any


class Cities:

    def __init__(self):
        self._cities = ["Paris", "Berlin", "Rome", "Madrid", "London"]

    def __len__(self):
        return len(self._cities)

    def __getitem__(self, pos: int):
        return self._cities[pos]


class CityIterator:

    def __init__(self, _cities: Any):
        self._cities = _cities
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._cities):
            raise StopIteration
        else:
            item = self._cities[self._index]
            self._index += 1
            return item


if __name__ == "__main__":
    cities = Cities()
    city_iterator = CityIterator(cities)
    for item in city_iterator:
        print(item)
