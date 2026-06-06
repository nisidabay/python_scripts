#-------------------------------------------------------------------------------
# Name:        memoization-1.py
# Purpose:
#
# Author:      clacmoy
#
# Created:     12/07/2021
# Copyright:   (c) clacmoy 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
from time import perf_counter

cache = {}

def memoization(num:int)-> int:
    if num in cache:
       print("Getting from cache ..")
       return cache[num]

    print("Computing ...")
    time.sleep(1)
    result = num * num
    cache[num] = result
    return result

def main():
    init = perf_counter()
    print(memoization(4))
    print(memoization(4))
    print(memoization(4))
    print(memoization(4))

    print(f"Process took: {perf_counter() - init:.2f} secs")

if __name__ == '__main__':
    main()
