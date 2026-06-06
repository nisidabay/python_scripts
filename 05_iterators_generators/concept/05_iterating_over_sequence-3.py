#!/usr/bin/python3
#############################################################################
# Idea from: Deep Dive 2
# Author: Carlos Lacaci Moya
# Description:Iterable vs Iterator
# Date: lun 25 jul 2022 08:31:13 CEST
# Dependencies:
#############################################################################

from typing import Sequence


class CitiesIter:
    """Iterator class of list of cities"""
    def __init__(self, seq: Sequence[str]):
        self.idx = 0
        self.seq = seq

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx >= len(self.seq):
            raise StopIteration
        else:
            result = self.seq[self.idx]
            self.idx += 1
            return result


if __name__ == "__main__":
    cyties = ["Madrid", "Cadiz", "Granada", "Málaga"]
    it = CitiesIter(cyties)
    for i in it:
        print(i)
