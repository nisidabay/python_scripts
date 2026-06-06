#!/usr/bin/env python

from typing import Any, Optional


class DoublyNode:
    """
    Represents a single node in a doubly linked list.

    Attributes:
        data: The data stored in the node.
        next: A reference to the next node in the list.
        prev: A reference to the previous node in the list.
    """

    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional['DoublyNode'] = None
        self.prev: Optional['DoublyNode'] = None

    def __repr__(self) -> str:
        return f"DoublyNode({self.data})"


class DoublyLinkedList:
    """
    Represents a doubly linked list.

    Attributes:
        head: The first node in the linked list. None if the list is empty.
        tail: The last node in the linked list. None if the list is empty.
    """

    def __init__(self):
        self.head: Optional[DoublyNode] = None
        self.tail: Optional[DoublyNode] = None
        self.length: int = 0

    def is_empty(self) -> bool:
        """Checks if the list is empty."""
        return self.head is None

    def __len__(self) -> int:
        """Returns the number of nodes in the list."""
        return self.length

    def display_forward(self) -> None:
        """Prints the list from head to tail."""
        if self.is_empty():
            print("DoublyLinkedList is empty.")
            return
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        print("Head -> " + " <-> ".join(elements) + " <- Tail(None)")

    def display_backward(self) -> None:
        """Prints the list from tail to head."""
        if self.is_empty():
            print("DoublyLinkedList is empty.")
            return
        elements = []
        current = self.tail
        while current:
            elements.append(str(current.data))
            current = current.prev
        print("Tail -> " + " <-> ".join(elements) + " <- Head(None)")

    # --- Insertion Methods ---
    def insert_at_head(self, data: Any) -> None:
        """Inserts a new node at the beginning of the list."""
        new_node = DoublyNode(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            if self.head:  # mypy check
                self.head.prev = new_node
            self.head = new_node
        self.length += 1
        print(f"Inserted {data} at head.")

    def append(self, data: Any) -> None:
        """Inserts a new node at the end of the list (alias for insert_at_tail)."""
        self.insert_at_tail(data)

    def insert_at_tail(self, data: Any) -> None:
        """Inserts a new node at the end of the list."""
        new_node = DoublyNode(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            if self.tail:  # mypy check
                self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1
        print(f"Inserted {data} at tail.")

    def insert_at_position(self, position: int, data: Any) -> None:
        """Inserts a new node at a specific position (0-indexed)."""
        if position < 0 or position > self.length:
            raise IndexError(
                f"Position {position} is out of bounds for list of length {self.length}.")

        if position == 0:
            self.insert_at_head(data)
            return
        if position == self.length:
            self.insert_at_tail(data)
            return

        new_node = DoublyNode(data)
        current_node = self.head
        for _ in range(position - 1):  # Traverse to the node *before* the target position
            if current_node:  # mypy check
                current_node = current_node.next
            else:  # Should not happen if position is valid
                raise RuntimeError(
                    "Unexpected error during list traversal for insertion.")

        if current_node and current_node.next:  # mypy checks
            new_node.next = current_node.next
            new_node.prev = current_node
            current_node.next.prev = new_node
            current_node.next = new_node
            self.length += 1
            print(f"Inserted {data} at position {position}.")
        else:
            # This case should be covered by boundary checks, but as a safeguard
            raise IndexError(
                "Could not insert at the specified position, node not found.")

    # --- Deletion Methods ---

    def delete_from_head(self) -> Any:
        """Deletes the node from the beginning of the list."""
        if self.is_empty():
            raise IndexError("Cannot delete from an empty list.")

        deleted_node_data = self.head.data  # type: ignore
        if self.head == self.tail:  # Only one node
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next  # type: ignore
            if self.head:  # mypy check
                self.head.prev = None
        self.length -= 1
        print(f"Deleted {deleted_node_data} from head.")
        return deleted_node_data

    def delete_from_tail(self) -> Any:
        """Deletes the node from the end of the list."""
        if self.is_empty():
            raise IndexError("Cannot delete from an empty list.")

        deleted_node_data = self.tail.data  # type: ignore
        if self.head == self.tail:  # Only one node
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev  # type: ignore
            if self.tail:  # mypy check
                self.tail.next = None
        self.length -= 1
        print(f"Deleted {deleted_node_data} from tail.")
        return deleted_node_data

    def delete_at_position(self, position: int) -> Any:
        """Deletes the node at a specific position (0-indexed)."""
        if self.is_empty():
            raise IndexError("Cannot delete from an empty list.")
        if position < 0 or position >= self.length:
            raise IndexError(
                f"Position {position} is out of bounds for deletion.")

        if position == 0:
            return self.delete_from_head()
        if position == self.length - 1:
            return self.delete_from_tail()

        current_node = self.head
        for _ in range(position):
            if current_node:  # mypy check
                current_node = current_node.next
            else:  # Should not happen
                raise RuntimeError(
                    "Unexpected error during list traversal for deletion.")

        if current_node and current_node.prev and current_node.next:  # mypy checks
            deleted_node_data = current_node.data
            current_node.prev.next = current_node.next
            current_node.next.prev = current_node.prev
            self.length -= 1
            print(f"Deleted {deleted_node_data} from position {position}.")
            return deleted_node_data
        else:
            # This case should be covered by boundary checks
            raise IndexError("Could not delete at the specified position.")

    def delete_by_value(self, value: Any) -> bool:
        """Deletes the first occurrence of a node with the given value."""
        if self.is_empty():
            print(f"Value {value} not found for deletion (list is empty).")
            return False

        current_node = self.head
        while current_node:
            if current_node.data == value:
                if current_node == self.head:
                    self.delete_from_head()
                elif current_node == self.tail:
                    self.delete_from_tail()
                else:
                    if current_node.prev and current_node.next:  # mypy checks
                        current_node.prev.next = current_node.next
                        current_node.next.prev = current_node.prev
                        self.length -= 1
                        print(f"Deleted node with value {value}.")
                return True
            current_node = current_node.next

        print(f"Value {value} not found for deletion.")
        return False

    # --- Search Method ---
    def search(self, value: Any) -> int:
        """Searches for a value and returns its 0-indexed position, or -1 if not found."""
        current = self.head
        position = 0
        while current:
            if current.data == value:
                print(f"Value {value} found at position {position}.")
                return position
            current = current.next
            position += 1
        print(f"Value {value} not found.")
        return -1


# --- Example Usage ---
if __name__ == "__main__":
    dll = DoublyLinkedList()
    print(f"Is list empty? {dll.is_empty()}")
    dll.display_forward()
    print("-" * 20)

    dll.append(10)
    dll.append(20)
    dll.insert_at_head(5)
    dll.display_forward()  # Head -> 5 <-> 10 <-> 20 <- Tail(None)
    dll.display_backward()  # Tail -> 20 <-> 10 <-> 5 <- Head(None)
    print(f"Length: {len(dll)}")
    print("-" * 20)

    dll.insert_at_position(1, 7)  # 5 <-> 7 <-> 10 <-> 20
    dll.display_forward()
    dll.insert_at_position(0, 2)  # 2 <-> 5 <-> 7 <-> 10 <-> 20
    dll.display_forward()
    dll.insert_at_position(len(dll), 30)  # Appends 30
    dll.display_forward()
    print(f"Length: {len(dll)}")
    print("-" * 20)

    print(f"Search for 10: {dll.search(10)}")  # Position 3
    print(f"Search for 100: {dll.search(100)}")
    print("-" * 20)

    dll.delete_by_value(7)
    dll.display_forward()
    dll.delete_from_head()
    dll.display_forward()
    dll.delete_from_tail()
    dll.display_forward()  # 5 <-> 10 <-> 20
    print(f"Length: {len(dll)}")
    print("-" * 20)

    dll.delete_at_position(1)  # Deletes 10. List: 5 <-> 20
    dll.display_forward()

    try:
        dll.delete_at_position(5)  # Out of bounds
    except IndexError as e:
        print(f"Error: {e}")

    dll.delete_from_tail()  # Deletes 20. List: 5
    dll.display_forward()
    dll.delete_from_head()  # Deletes 5. List: empty
    dll.display_forward()
    print(f"Is list empty? {dll.is_empty()}")
    print(f"Length: {len(dll)}")
