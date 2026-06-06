#-------------------------------------------------------------------------------
# Name:        memoization-2.py
# Purpose:
#
# Author:      clacmoy
#
# Created:     12/07/2021
# Copyright:   (c) clacmoy 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class Node:
  def __init__(self, key, val):
      self.key = key
      self.val = val
      self.next = None
      self.prev = None

class LRUCache:
  cache_limit = 3

  def __init__(self, func):
      self.func = func
      self.cache = {}
      self.head = Node(0,0)
      self.tail = Node(0,0)
      self.head.next = self.tail
      self.tail.prev = self.head

if __name__ == '__main__':
    main()
