#!/usr/bin/env python

from typing import Any, Optional


class Node:  # Reusing the same Node class as in Singly Linked List
    """
    Represents a single node in a linked list.
    """

    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional['Node'] = None

    def __repr__(self) -> str:
        return f"Node({self.data})"


class CircularLinkedList:
    """
    Represents a singly circular linked list.

    Attributes:
        head: The first node in the linked list. None if the list is empty.
        tail: The last node in the list. In a circular list, tail.next points to head.
              Keeping a tail pointer helps with O(1) appends and head insertions.
    """

    def __init__(self):
        self.head: Optional[Node] = None
        # Explicitly track tail for efficiency
        self.tail: Optional[Node] = None
        self.length: int = 0

    def is_empty(self) -> bool:
        """Checks if the list is empty."""
        return self.head is None

    def __len__(self) -> int:
        """Returns the number of nodes in the list."""
        return self.length

    def display(self) -> None:
        """Prints the circular list elements, starting from the head."""
        if self.is_empty():
            print("CircularLinkedList is empty.")
            return

        elements = []
        current = self.head
        # To prevent infinite loop in case of malformed list (though unlikely with current logic)
        count = 0
        # The loop condition must handle the circularity.
        # We iterate self.length times, or until we return to head if we didn't store length.
        while current and count < self.length:
            elements.append(str(current.data))
            current = current.next
            count += 1
            # An alternative loop:
            # elements.append(str(current.data))
            # current = current.next
            # if current == self.head:
            #    break

        print("Head -> " + " -> ".join(elements) +
              f" -> (Back to Head: {self.head.data if self.head else 'None'})")

    # --- Insertion Methods ---

    def insert_at_head(self, data: Any) -> None:
        """Inserts a new node at the 'beginning' (new head) of the circular list."""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head  # Points to itself
        else:
            new_node.next = self.head
            self.head = new_node
            if self.tail:  # mypy check
                self.tail.next = self.head  # Crucial: old tail now points to new head
        self.length += 1
        print(f"Inserted {data} at head.")

    def append(self, data: Any) -> None:
        """Inserts a new node at the end of the circular list (becomes new tail)."""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head  # Points to itself
        else:
            if self.tail:  # mypy check
                self.tail.next = new_node
            self.tail = new_node
            self.tail.next = self.head  # New tail points back to head
        self.length += 1
        print(f"Appended {data}.")

    def insert_at_position(self, position: int, data: Any) -> None:
        """Inserts a node at a specific position (0-indexed)."""
        if position < 0 or position > self.length:
            raise IndexError(
                f"Position {position} is out of bounds for list of length {self.length}.")

        if position == 0:
            self.insert_at_head(data)
            return
        if position == self.length:  # Equivalent to append
            self.append(data)
            return

        new_node = Node(data)
        current_node = self.head
        # Traverse to the node *before* the target position
        for _ in range(position - 1):
            if current_node:  # mypy check
                current_node = current_node.next
            else:  # Should not happen
                raise RuntimeError(
                    "Unexpected error during list traversal for insertion.")

        if current_node:  # mypy check
            new_node.next = current_node.next
            current_node.next = new_node
            self.length += 1
            print(f"Inserted {data} at position {position}.")
        else:
            raise IndexError("Could not insert at specified position.")

    # --- Deletion Methods ---

    def delete_from_head(self) -> Any:
        """Deletes the head node."""
        if self.is_empty():
            raise IndexError("Cannot delete from an empty list.")

        deleted_node_data = self.head.data  # type: ignore
        if self.head == self.tail:  # Only one node
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next  # type: ignore
            if self.tail:  # mypy check
                self.tail.next = self.head  # Tail points to new head
        self.length -= 1
        print(f"Deleted {deleted_node_data} from head.")
        return deleted_node_data

    def delete_from_tail(self) -> Any:
        """Deletes the tail node."""
        if self.is_empty():
            raise IndexError("Cannot delete from an empty list.")

        deleted_node_data = self.tail.data  # type: ignore
        if self.head == self.tail:  # Only one node
            self.head = None
            self.tail = None
        else:
            # Need to find the node *before* the tail
            current = self.head
            while current and current.next != self.tail:
                current = current.next

            if current:  # mypy check
                current.next = self.head  # New tail's next points to head
                self.tail = current
            else:  # Should not happen if list has >1 elements
                raise RuntimeError("Error finding node before tail.")

        self.length -= 1
        print(f"Deleted {deleted_node_data} from tail.")
        return deleted_node_data

    def delete_by_value(self, value: Any) -> bool:
        """Deletes the first occurrence of a node with the given value."""
        if self.is_empty():
            print(f"Value {value} not found for deletion (list is empty).")
            return False

        # Case 1: Value is at the head
        if self.head.data == value:  # type: ignore
            self.delete_from_head()
            return True

        # Case 2: Value is elsewhere (or is the tail)
        current = self.head
        prev_node = None
        # Traverse until we find the value or loop back to head
        # We must stop *before* current becomes head again if value not found earlier
        # or if current.next is head (meaning current is tail)

        # Iterate up to length -1 times because head case is handled
        for _ in range(self.length - 1):
            if not current or not current.next:
                break  # Should not happen in a well-formed circular list
            prev_node = current
            current = current.next
            if current.data == value:
                if current == self.tail:  # Value is at the tail
                    self.delete_from_tail()
                else:  # Value is in the middle
                    prev_node.next = current.next
                    self.length -= 1
                    print(f"Deleted node with value {value}.")
                return True
            # Completed a full circle without finding (after head)
            if current == self.head:
                break

        print(f"Value {value} not found for deletion.")
        return False

    # --- Search Method ---
    def search(self, value: Any) -> int:
        """Searches for a value and returns its 0-indexed position, or -1 if not found."""
        if self.is_empty():
            return -1

        current = self.head
        position = 0
        for _ in range(self.length):  # Iterate up to self.length times
            if current.data == value:  # type: ignore
                print(f"Value {value} found at position {position}.")
                return position
            current = current.next  # type: ignore
            position += 1
            # Optimization: if we've looped and not found.
            if current == self.head and position > 0:
                break  # This condition is covered by range(self.length)

        print(f"Value {value} not found.")
        return -1


# --- Example Usage ---
if __name__ == "__main__":
    cll = CircularLinkedList()
    print(f"Is list empty? {cll.is_empty()}")
    cll.display()
    print("-" * 20)

    cll.append(10)
    cll.append(20)
    cll.insert_at_head(5)
    cll.display()  # Head -> 5 -> 10 -> 20 -> (Back to Head: 5)
    print(f"Length: {len(cll)}")
    if cll.head and cll.tail:
        print(
            f"Head: {cll.head.data}, Tail: {cll.tail.data}, Tail.next: {cll.tail.next.data if cll.tail.next else 'None'}")
    print("-" * 20)

    cll.insert_at_position(1, 7)  # 5 -> 7 -> 10 -> 20
    cll.display()
    cll.insert_at_position(0, 2)  # 2 -> 5 -> 7 -> 10 -> 20
    cll.display()
    cll.insert_at_position(len(cll), 30)  # Appends 30
    cll.display()
    print(f"Length: {len(cll)}")
    if cll.head and cll.tail:
        print(
            f"Head: {cll.head.data}, Tail: {cll.tail.data}, Tail.next: {cll.tail.next.data if cll.tail.next else 'None'}")
    print("-" * 20)

    print(f"Search for 10: {cll.search(10)}")  # Position 3
    print(f"Search for 100: {cll.search(100)}")
    print("-" * 20)

    cll.delete_by_value(7)
    cll.display()
    cll.delete_from_head()
    cll.display()
    cll.delete_from_tail()  # Tail was 30, new tail is 20
    cll.display()  # 5 -> 10 -> 20 -> (Back to Head: 5)
    print(f"Length: {len(cll)}")
    if cll.head and cll.tail:
        print(
            f"Head: {cll.head.data}, Tail: {cll.tail.data}, Tail.next: {cll.tail.next.data if cll.tail.next else 'None'}")
    print("-" * 20)

    # Current list: 5 -> 10 -> 20
    cll.delete_by_value(10)  # 5 -> 20
    cll.display()
    cll.delete_by_value(5)  # 20
    cll.display()
    cll.delete_by_value(20)  # empty
    cll.display()
    print(f"Is list empty? {cll.is_empty()}")
    print(f"Length: {len(cll)}")

    # Test deleting from list with one element
    cll.append(55)
    cll.display()
    cll.delete_from_head()
    cll.display()
