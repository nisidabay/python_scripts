# Collections — namedtuple, OrderedDict, UserString, linked lists, permutations

## Quick Start
```bash
python 06_namedtuple.py
python 06_namedtuple_wc.py
python 06_dict_order.py
python 06_userstring.py
python 06_Nodo.py
python 06_linked_list.py
python 06_linked_list_gemini.py
python 06_double_linked_list_gemini.py
python 06_circular_linked_list_gemini.py
python 06_permutations.py
python 06_permutations_2.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `06_namedtuple.py` | Lightweight immutable data objects | `namedtuple("DivMod", "quotient remainder")`, `defaults=["not assigned"]` |
| `06_namedtuple_wc.py` | Namedtuple for structured results (like `wc`) | `counter = namedtuple("Counter", ["lines","words","chars"])` |
| `06_dict_order.py` | Regular dict vs OrderedDict equality | Regular dicts compare by content, `OrderedDict` compares by order too |
| `06_userstring.py` | Custom string subclass via `UserString` | `class MaskCreditCard(UserString)`, override `__str__`, access `self.data` |
| `06_Nodo.py` | Recursive linked list with dataclass | `@dataclass class Nodo`, recursive `agregar()` and `listar()` |
| `06_linked_list.py` | Singly linked list from scratch | `Node` with `value`/`next`, insert/delete at head/tail/position |
| `06_linked_list_gemini.py` | Full-featured singly linked list | `__len__`, `__str__`, `insert_at_position`, `delete_by_value`, `search` |
| `06_double_linked_list_gemini.py` | Doubly linked list with prev/next pointers | `DoublyNode.prev`, `display_forward/backward`, O(1) tail operations |
| `06_circular_linked_list_gemini.py` | Circular linked list (tail→head) | `tail.next = self.head`, no null terminator, `for _ in range(self.length)` |
| `06_permutations.py` | Recursive string permutations | Pick each letter, recurse on remainder, accumulate |
| `06_permutations_2.py` | Permutations with `itertools.product` | Recursive divide-and-conquer, `itertools.product` for cross-join |

## Common Patterns
```python
from collections import namedtuple, OrderedDict, UserString

# Namedtuple — lightweight immutable struct
Point = namedtuple("Point", ["x", "y", "z"], defaults=[0, 0, 0])
p = Point(5, 3)
print(p.x, p.y)  # attribute access, not index

# Namedtuple with defaults (rightmost first)
Employee = namedtuple("Employee", ["name", "job", "phone"],
                      defaults=["not assigned"])

# OrderedDict — order-sensitive equality
from collections import OrderedDict
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
od1 == od2  # False — order matters

# UserString — customize string behavior
class Masked(UserString):
    def __str__(self):
        return "*" * (len(self.data) - 4) + self.data[-4:]

# Singly linked list building blocks
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_head(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

# Doubly linked: add prev pointer
class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

# Circular linked: tail.next → head
class CircularList:
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
            new_node.next = self.head     # points to itself
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.tail.next = self.head    # close the circle

# Recursive permutations
def permute(s):
    if len(s) == 0:
        return ['']
    result = []
    for i, ch in enumerate(s):
        for rest in permute(s[:i] + s[i+1:]):
            result.append(ch + rest)
    return result
```

## Now Build Your Own
Write `collection_playground.py` that:
1. Defines a `namedtuple` `Student(name, grade, subjects)` with `defaults` for `subjects=[]`.
2. Implements a `TrackedDict(UserDict)` subclass that logs every `__setitem__` call with a timestamp.
3. Builds a **singly linked list** `Stack` class with `push`, `pop`, `peek`, and `__len__` (LIFO, all O(1)).
4. Implements `generate_anagrams(word)` using the recursive permutation pattern — return a set of all unique letter arrangements.
5. Uses `itertools.combinations` to list all 3-element subsets of `{'a','b','c','d','e'}`.
