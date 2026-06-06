#!/usr/bin/python3
# From Python 3: Deep Dive (Part 4 - OOP)
# Adding methods at runtime
from types import MethodType


class Person:
    def __init__(self, name):
        self.name = name

    def register_do_work(self, func):
        # setattr(self, "_do_work", MethodType(func, self))
        self._do_work = MethodType(func, self)

    def do_work(self):
        if do_work_method := getattr(self, "_do_work", None):
            return do_work_method()

        else:
            raise AttributeError("You must first register a do_work_method")


if __name__ == "__main__":
    math_teacher = Person("John")

    def work_math(self):
        return f"{self.name} will teach differentials today."

    math_teacher.register_do_work(work_math)
    print(math_teacher.do_work())

    english_teacher = Person("Alex")

    def work_english(self):
        return f"{self.name} will teach Hamlet today."

    english_teacher.register_do_work(work_english)
    print(english_teacher.do_work())
