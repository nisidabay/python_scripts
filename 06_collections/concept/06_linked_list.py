#!/usr/bin/python3
#
# from: Learn Data Structure Array, Linked List, Stack & Queue using Python in
# 5 minutes. BASU,s

from typing import Optional


class Node:
    """Represents a node in the linked list."""

    def __init__(self, value: int) -> None:
        """
        Initialize a new Node instance.

        Args:
            value (int): The value to be stored in the node.
        """
        self.value = value
        self.next: Optional[Node] = None


class LinkedList:
    """Represents a singly linked list."""

    def __init__(self):
        """Initialize an empty linked list."""
        self.head: Optional[Node] = None

    def show_nodes(self) -> None:
        """
        Display the linked list elements.

        Prints the linked list elements in the format: "value -> value -> ... -> NULL".
        """
        temp = self.head
        while temp:
            print(f"{temp.value} ->", end="")
            temp = temp.next
        print("NULL", end="")

    def add_beginning(self, new_val: int) -> None:
        """
        Add a new node with the given value at the beginning of the linked list.

        Args:
            new_val (int): The value for the new node.
        """
        temp = self.head
        self.head = Node(new_val)
        self.head.next = temp

    def add_after(self, prev_node: Node, new_val: int) -> None:
        """
        Add a new node with the given value after the specified node.

        Args:
            prev_node (Node): The node after which the new node will be added.
            new_val (int): The value for the new node.
        """
        if prev_node is None:
            print("Previous node must be in the list.")
            return

        new_node = Node(new_val)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def add_end(self, new_val: int) -> None:
        """
        Add a new node with the given value at the end of the linked list.

        Args:
            new_val (int): The value for the new node.
        """
        new_node = Node(new_val)
        if not self.head:
            self.head = new_node
            return

        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def delete_node(self, key: int) -> None:
        """
        Delete the first occurrence of a node with the given value from the linked list.

        Args:
            key (int): The value of the node to be deleted.
        """
        temp = self.head

        if temp is not None and temp.value == key:
            self.head = temp.next
            temp = None
            return

        prev = None
        while temp is not None and temp.value != key:
            prev = temp
            temp = temp.next

        if temp is None:
            return

        prev.next = temp.next
        temp = None


if __name__ == "__main__":
    l = LinkedList()
    l.head = Node(5)
    n2 = Node(2)
    n3 = Node(3)
    n2.next = n3
    l.head.next = n2

    l.add_beginning(10)
    l.add_after(n2, 5.5)
    l.add_end(20)

    print("Original linked list:")
    l.show_nodes()

    l.delete_node(5)  # Delete a node with value 5
    print("\nLinked list after deleting node with value 5:")
    l.show_nodes()
