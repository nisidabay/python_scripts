#!/usr/bin/python3
# From Python 3: Deep Dive (Part 4 - OOP)
# classmethod usage

# In this output, you can see that the id of ob1 (the instance created with
# __init__()) and the id of the MyClass class itself are different. This is
# because they are separate objects in memory.
#
# When you create an instance of a class with MyClass(1), Python creates a new
# instance of the MyClass class in memory and assigns it a unique memory address.
# When you call MyClass.from_string("1"), another new instance of the MyClass
# class is created in memory, with a different memory address.
#
# The id function is used to print the memory address of the self.x and cls.x
# attributes, and you can see that they have the same memory address, indicating
# that they are referring to the same object in memory (in this case, the integer
# object with value 1).
#
# When you call int(string) to convert the input string to an integer in the
# from_string() method, Python first checks if an integer object with the same
# value already exists in memory. If it does, Python will reuse that object
# instead of creating a new one. This is known as integer interning and is an
# optimization that can save memory and improve performance.
#
# To summarize, in this example the id of ob1 and the id of the MyClass class
# itself are different, but the id of self.x and cls.x are the same, indicating
# that they are referring to the same object in memory.


class MyClass:
    def __init__(self, x):
        self.x = x
        print("__init__")
        print(f"self.x={self.x}")
        print(f"id self.x={id(self.x)}")

    @classmethod
    def from_string(cls, string):
        x = int(string)
        print("__classmethod__")
        print(f"cls.x={x}")
        print(f"id cls.x={id(x)}")

        return cls(x)


if __name__ == "__main__":
    ob1 = MyClass(1)
    print(f"ob1.id = {id(ob1)}")
    print("----")
    MyClass.from_string("1")
    print(f"MyClass.id = {id(MyClass)}")
