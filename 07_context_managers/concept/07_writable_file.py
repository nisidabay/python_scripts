#!/usr/bin/env python
#
# Implementation of a contextmanager
from typing import Any, TextIO


class WritableFile:
    """
    Context manager for writing to a file.

    This class provides a way to write data to a file and ensures the file is
    properly closed after use. It acts as a context manager, allowing you to use
    it with the 'with' statement.

    Attributes:
        file_path (str): The path to the file to be written to.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes a WritableFile object.

        Args:
            file_path (str): The path to the file to be written to.
        """
        self.file_path = file_path

    def __enter__(self) -> TextIO:
        """
        Opens the file in write mode and returns a TextIO object.

        Returns:
            TextIO: A TextIO object representing the open file.
        """
        self.file_obj = open(self.file_path, mode="w")
        return self.file_obj

    def __exit__(self, exc_type: Any, exc_value: Any, exc_tb: Any) -> None:
        """
        Closes the file if it was opened successfully.

        Args:
            exc_type (Any): The type of exception that occurred.
            exc_value (Any): The value of the exception that occurred.
            exc_tb (Any): The traceback of the exception that occurred.
        """
        if self.file_obj:
            self.file_obj.close()


if __name__ == "__main__":
    with WritableFile("file.txt") as file:
        file.write("Context manager")
