#!/usr/bin/env python

from typing import Any, Optional


class Node:
    """
    Represents a single node in a linked list.

    Attributes:
        data: The data stored in the node.
        next: A reference to the next node in the list, or None if it's the last node.
    """

    def __init__(self, data: Any):
        """
        Initializes a new Node.

        Args:
            data: The data to be stored in the node.
        """
        self.data: Any = data
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        """
        Returns a developer-friendly string representation of the Node.

        Returns:
            A string in the format "Node(data_value)".
        """
        return f"Node({self.data})"


class LinkedList:
    """
    Represents a singly linked list.

    Attributes:
        head: The first node in the linked list. None if the list is empty.
    """

    def __init__(self):
        """
        Initializes an empty LinkedList.
        """
        self.head: Optional[Node] = None

    def is_empty(self) -> bool:
        """
        Checks if the linked list is empty.

        Returns:
            True if the list is empty, False otherwise.
        """
        return self.head is None

    def __len__(self) -> int:
        """
        Returns the number of nodes in the linked list.

        Returns:
            The length of the list.
        """
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the linked list.

        Returns:
            A string in the format "Head -> Node1_data -> Node2_data -> ... -> Tail(None)".
        """
        nodes_str = []
        current = self.head
        if not current:
            return "LinkedList is empty."
        while current:
            nodes_str.append(str(current.data))
            current = current.next
        return "Head -> " + " -> ".join(nodes_str) + " -> Tail(None)"

    def display(self) -> None:
        """
        Prints the string representation of the linked list to the console.
        """
        print(str(self))

    # --- Insertion Methods ---

    def insert_at_head(self, data: Any) -> None:
        """
        Inserts a new node with the given data at the beginning of the list.

        Args:
            data: The data for the new node.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        print(f"Inserted {data} at head.")

    def append(self, data: Any) -> None:
        """
        Inserts a new node with the given data at the end of the list.
        This is an alias for insert_at_tail.

        Args:
            data: The data for the new node.
        """
        self.insert_at_tail(data)

    def insert_at_tail(self, data: Any) -> None:
        """
        Inserts a new node with the given data at the end of the list.

        Args:
            data: The data for the new node.
        """
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            print(f"Inserted {data} at tail (list was empty).")
            return

        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
        print(f"Inserted {data} at tail.")

    def insert_at_position(self, position: int, data: Any) -> None:
        """
        Inserts a new node with the given data at a specific position (0-indexed).

        Args:
            position: The 0-based index where the new node should be inserted.
            data: The data for the new node.

        Raises:
            IndexError: If the position is negative or greater than the list length.
        """
        if position < 0:
            raise IndexError("Position cannot be negative.")

        if position == 0:
            self.insert_at_head(data)
            return

        new_node = Node(data)
        current_node = self.head
        current_position = 0

        # Traverse to the node just before the target position
        while current_node and current_position < position - 1:
            current_node = current_node.next
            current_position += 1

        # Position is out of bounds (greater than length)
        if current_node is None:
            # If position is exactly the length, it's an append operation
            if position == len(self):
                self.append(data)
                return
            raise IndexError(
                f"Position {position} is out of bounds for list of length {len(self)}.")

        new_node.next = current_node.next
        current_node.next = new_node
        print(f"Inserted {data} at position {position}.")

    # --- Deletion Methods ---

    def delete_from_head(self) -> Any:
        """
        Deletes the node from the beginning of the list.

        Returns:
            The data of the deleted node.

        Raises:
            IndexError: If the list is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot delete from an empty list.")

        deleted_node_data = self.head.data  # type: ignore
        self.head = self.head.next  # type: ignore
        print(f"Deleted {deleted_node_data} from head.")
        return deleted_node_data

    def delete_from_tail(self) -> Any:
        """
        Deletes the node from the end of the list.

        Returns:
            The data of the deleted node.

        Raises:
            IndexError: If the list is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot delete from an empty list.")

        # If there's only one node
        if self.head.next is None:  # type: ignore
            deleted_node_data = self.head.data  # type: ignore
            self.head = None
            print(
                f"Deleted {deleted_node_data} from tail (was the only node).")
            return deleted_node_data

        # Traverse to the second to last node
        second_last_node = self.head
        while second_last_node.next and second_last_node.next.next:  # type: ignore
            second_last_node = second_last_node.next

        deleted_node_data = second_last_node.next.data  # type: ignore
        second_last_node.next = None
        print(f"Deleted {deleted_node_data} from tail.")
        return deleted_node_data

    def delete_at_position(self, position: int) -> Any:
        """
        Deletes the node at a specific position (0-indexed).

        Args:
            position: The 0-based index of the node to delete.

        Returns:
            The data of the deleted node.

        Raises:
            IndexError: If the position is invalid or the list is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot delete from an empty list.")

        if position < 0:
            raise IndexError("Position cannot be negative.")

        if position == 0:
            return self.delete_from_head()

        current_node = self.head
        current_position = 0
        previous_node = None

        # Traverse to the node at the target position
        while current_node and current_position < position:
            previous_node = current_node
            current_node = current_node.next
            current_position += 1

        if current_node is None:  # Position is out of bounds
            raise IndexError(
                f"Position {position} is out of bounds for deletion.")

        if previous_node:  # Should always be true if position > 0 and valid
            previous_node.next = current_node.next
            deleted_node_data = current_node.data
            print(f"Deleted {deleted_node_data} from position {position}.")
            return deleted_node_data
        else:
            # This case should ideally not be reached if position > 0 due to prior checks
            # but as a safeguard:
            raise IndexError("Error in delete_at_position logic.")

    def delete_by_value(self, value: Any) -> bool:
        """
        Deletes the first occurrence of a node with the given value.

        Args:
            value: The value to search for and delete.

        Returns:
            True if a node with the value was found and deleted, False otherwise.
        """
        if self.is_empty():
            print(f"Value {value} not found for deletion (list is empty).")
            return False

        # If the head node itself holds the value
        if self.head.data == value:  # type: ignore
            self.head = self.head.next  # type: ignore
            print(f"Deleted node with value {value} (was head).")
            return True

        current_node = self.head
        previous_node = None
        while current_node and current_node.data != value:
            previous_node = current_node
            current_node = current_node.next

        if current_node is None:  # Value not found
            print(f"Value {value} not found for deletion.")
            return False

        # Value found at current_node
        if previous_node:  # Should always be true if not head
            previous_node.next = current_node.next
            print(f"Deleted node with value {value}.")
            return True
        return False  # Should not be reached if logic is correct

    # --- Search Methods ---

    def search(self, value: Any) -> int:
        """
        Searches for the first occurrence of a value in the list.

        Args:
            value: The value to search for.

        Returns:
            The 0-indexed position of the first node containing the value,
            or -1 if the value is not found.
        """
        current_node = self.head
        position = 0
        while current_node:
            if current_node.data == value:
                print(f"Value {value} found at position {position}.")
                return position
            current_node = current_node.next
            position += 1

        print(f"Value {value} not found in the list.")
        return -1

    def get_node_at_position(self, position: int) -> Optional[Node]:
        """
        Retrieves the node at a specific position (0-indexed).

        Args:
            position: The 0-based index of the node to retrieve.

        Returns:
            The Node at the specified position, or None if the position is invalid.
        """
        if position < 0:
            print(
                f"Invalid position: {position}. Position cannot be negative.")
            return None

        current_node = self.head
        current_position = 0
        while current_node and current_position < position:
            current_node = current_node.next
            current_position += 1

        if current_node:
            return current_node
        else:
            print(f"No node found at position {position} (out of bounds).")
            return None


# --- Example Usage ---
if __name__ == "__main__":
    my_list = LinkedList()
    print(f"Is list empty? {my_list.is_empty()}")
    print(f"List length: {len(my_list)}")
    my_list.display()
    print("-" * 20)

    my_list.append(10)  # Insert at tail
    my_list.append(20)
    my_list.insert_at_head(5)  # Insert at head
    my_list.display()
    print(f"List length: {len(my_list)}")
    print("-" * 20)

    my_list.insert_at_position(1, 7)  # 5 -> 7 -> 10 -> 20
    my_list.display()
    my_list.insert_at_position(0, 2)  # 2 -> 5 -> 7 -> 10 -> 20
    my_list.display()
    my_list.insert_at_position(5, 30)  # 2 -> 5 -> 7 -> 10 -> 20 -> 30 (append)
    my_list.display()
    print(f"List length: {len(my_list)}")
    print("-" * 20)

    # Test insertion at out-of-bounds (end)
    try:
        my_list.insert_at_position(len(my_list), 40)  # Should append 40
        my_list.display()
    except IndexError as e:
        print(f"Error: {e}")

    # Test insertion at out-of-bounds (far end)
    try:
        my_list.insert_at_position(10, 99)  # Should raise IndexError
    except IndexError as e:
        print(f"Error: {e}")
    print("-" * 20)

    print(f"Searching for 10: Position {my_list.search(10)}")
    print(f"Searching for 100: Position {my_list.search(100)}")
    print("-" * 20)

    node_at_2 = my_list.get_node_at_position(2)
    if node_at_2:
        print(f"Node at position 2: {node_at_2.data}")
    node_at_10 = my_list.get_node_at_position(10)  # Out of bounds
    print("-" * 20)

    my_list.delete_by_value(7)  # 2 -> 5 -> 10 -> 20 -> 30 -> 40
    my_list.display()
    my_list.delete_by_value(2)  # 5 -> 10 -> 20 -> 30 -> 40 (delete head)
    my_list.display()
    my_list.delete_by_value(40)  # 5 -> 10 -> 20 -> 30 (delete tail)
    my_list.display()
    my_list.delete_by_value(100)  # Value not found
    my_list.display()
    print(f"List length: {len(my_list)}")
    print("-" * 20)

    my_list.delete_from_head()  # 10 -> 20 -> 30
    my_list.display()
    my_list.delete_from_tail()  # 10 -> 20
    my_list.display()
    print(f"List length: {len(my_list)}")
    print("-" * 20)

    # Current list: 10 -> 20
    my_list.delete_at_position(1)  # Deletes 20. List: 10
    my_list.display()

    try:
        my_list.delete_at_position(1)  # Error: out of bounds
    except IndexError as e:
        print(f"Error: {e}")

    my_list.delete_at_position(0)  # Deletes 10. List: empty
    my_list.display()
    print(f"List length: {len(my_list)}")
    print(f"Is list empty? {my_list.is_empty()}")
    print("-" * 20)

    try:
        my_list.delete_from_head()  # Error: empty list
    except IndexError as e:
        print(f"Error: {e}")

    # Test deleting from tail when only one node
    my_list.append(55)
    my_list.display()
    my_list.delete_from_tail()
    my_list.display()
    print(f"Is list empty? {my_list.is_empty()}")
