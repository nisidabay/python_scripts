#!/usr/bin/python3
import os


def tree(startpath):
    # use os.walk to recursively iterate over all directories and files in startpath and its subdirectories
    for root, dirs, files in os.walk(startpath):
        # calculate the level of indentation based on how deep the current directory is in the directory tree
        level = root.count(os.sep)
        # create a string of spaces to use as indentation for the current directory
        indent = " " * 2 * (level)
        # print the name of the current directory, preceded by the appropriate amount of indentation
        print(f"{indent}{os.path.basename(root)}/")
        # create another indentation string for the files in the current directory
        subindent = " " * 2 * (level + 2)
        # iterate over the files in the current directory and print their names, preceded by the appropriate amount of indentation
        for file in files:
            print(f"{subindent}{file}")


if __name__ == "__main__":
    # prompt the user to enter the path of the directory to generate a tree for
    startpath = os.path.expanduser("~/Documents")  # or pass as argument
    # call the tree() function with the user-specified startpath
    tree(startpath)
