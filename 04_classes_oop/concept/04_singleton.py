#!/usr/bin/python3
"""
Module: DesignPatternsExample
Description: This module demonstrates the concept of design patterns in software development.
"""


class Singleton:
    _instance = None

    @staticmethod
    def get_instance():
        if Singleton._instance is None:
            Singleton._instance = Singleton()
        return Singleton._instance


# Usage of Singleton design pattern
instance1 = Singleton.get_instance()
instance2 = Singleton.get_instance()

print(instance1 is instance2)  # Outputs: True (both instances are the same)
