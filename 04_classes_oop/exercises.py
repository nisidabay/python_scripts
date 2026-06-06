#!/usr/bin/env python3
# exercises.py — Group 04: Classes & OOP
# 4 solved exercises + BONUS. Run: python3 exercises.py

import csv
import json
import math
from io import StringIO
from pathlib import Path


# ============================================================
# Exercise 1: @classmethod as alternative constructor
#            (from_csv, from_json)
# ============================================================

class Book:
    """A book with title, author, and publication year."""

    def __init__(self, title: str, author: str, year: int):
        self.title = title
        self.author = author
        self.year = year

    def __repr__(self) -> str:
        return f"Book({self.title!r}, {self.author!r}, {self.year})"

    @classmethod
    def from_csv(cls, line: str):
        """Alternative constructor: parse a CSV line into a Book.

        Expected format: title,author,year
        """
        title, author, year_str = line.strip().split(",")
        return cls(title.strip(), author.strip(), int(year_str.strip()))

    @classmethod
    def from_json(cls, text: str):
        """Alternative constructor: parse a JSON string into a Book."""
        data = json.loads(text)
        return cls(**data)  # unpack dict keys → constructor args

print("Exercise 1:")
# Standard constructor
b1 = Book("El Quijote", "Miguel de Cervantes", 1605)
print(f"  Standard:  {b1}")

# Build from CSV
b2 = Book.from_csv("Cien años de soledad, Gabriel García Márquez, 1967")
print(f"  From CSV:  {b2}")
assert b2.title == "Cien años de soledad"
assert b2.year == 1967

# Build from JSON
b3 = Book.from_json('{"title": "Rayuela", "author": "Julio Cortázar", "year": 1963}')
print(f"  From JSON: {b3}")
assert b3.author == "Julio Cortázar"
print("---")


# ============================================================
# Exercise 2: @property with getter/setter for validation
# ============================================================

class Person:
    """Person with age validated via property setter."""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age  # triggers setter validation

    @property
    def age(self) -> int:
        """Getter: return the internal _age."""
        return self._age

    @age.setter
    def age(self, value: int):
        """Setter: validate before storing."""
        if not isinstance(value, int):
            raise TypeError(f"Age must be int, got {type(value).__name__}")
        if value < 0 or value > 150:
            raise ValueError(f"Age {value} out of plausible range (0-150)")
        self._age = value

print("Exercise 2:")
carlos = Person("Carlos", 34)
print(f"  {carlos.name} is {carlos.age} years old")
assert carlos.age == 34

# Setter validation
try:
    carlos.age = -5
except ValueError as e:
    print(f"  Caught ValueError: {e}")

try:
    carlos.age = "treinta"
except TypeError as e:
    print(f"  Caught TypeError: {e}")

# Valid update
carlos.age = 35
print(f"  Updated: {carlos.name} is now {carlos.age}")
assert carlos.age == 35
print("---")


# ============================================================
# Exercise 3: Composition — Car has Engine, Wheels (NOT
#            inheritance)
# ============================================================

class Engine:
    """Engine component — standalone, reusable."""
    def __init__(self, horsepower: int):
        self.hp = horsepower
        self._running = False

    def start(self) -> str:
        self._running = True
        return f"Vroom! ({self.hp} HP)"

    def stop(self) -> str:
        self._running = False
        return "Engine off."

class Wheel:
    """Wheel component."""
    def __init__(self, position: str, size: int = 17):
        self.position = position  # e.g. 'front-left'
        self.size = size

    def __repr__(self) -> str:
        return f"Wheel({self.position}, {self.size}\")"

class Car:
    """Car built via composition — has Engine and Wheels, doesn't inherit them."""
    def __init__(self, make: str, model: str, hp: int):
        self.make = make
        self.model = model
        # Composition: Car *owns* these objects
        self.engine = Engine(hp)
        self.wheels = [
            Wheel("front-left"), Wheel("front-right"),
            Wheel("rear-left"), Wheel("rear-right"),
        ]

    def start(self) -> None:
        print(f"  Starting {self.make} {self.model}: {self.engine.start()}")

    def info(self) -> str:
        return (f"{self.make} {self.model} — "
                f"{self.engine.hp} HP, "
                f"{len(self.wheels)} wheels")

print("Exercise 3:")
car = Car("SEAT", "Ibiza", 150)
print(f"  {car.info()}")
car.start()
assert car.engine._running is True
assert len(car.wheels) == 4
assert car.wheels[0].position == "front-left"
# This IS-A test: Car is NOT an Engine (composition, not inheritance)
assert not isinstance(car, Engine)
print("---")


# ============================================================
# Exercise 4: Singleton pattern (module-level instance)
# ============================================================

# In Python, the simplest singleton is a module-level instance.
# Modules are imported only once and cached in sys.modules.

class AppConfig:
    """Application configuration — only one instance should exist."""
    def __init__(self):
        self._settings: dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        self._settings[key] = value

    def get(self, key: str, default: str = "") -> str:
        return self._settings.get(key, default)

    def __repr__(self) -> str:
        return f"AppConfig({self._settings})"

# Module-level instance — this is the singleton
CONFIG = AppConfig()

print("Exercise 4:")
# Two "imports" would return the same object because modules are cached
# Simulate that: any code that does 'from exercises import CONFIG' gets the SAME one
import sys
import importlib

module = sys.modules[__name__]
instance_a = module.CONFIG
instance_b = getattr(importlib.import_module(__name__), "CONFIG")
print(f"  Are they the same object? {instance_a is instance_b}")
assert instance_a is instance_b, "Module-level singleton should be unique"

# Use it
CONFIG.set("theme", "dark")
CONFIG.set("lang", "es")
print(f"  {CONFIG}")
assert CONFIG.get("theme") == "dark"
assert CONFIG.get("lang") == "es"
print("---")


# ============================================================
# BONUS: Descriptor that validates type on attribute assignment
# ============================================================

class Typed:
    """Descriptor: enforce a specific type on an attribute.

    Uses __set_name__ (Python 3.6+) so the attribute name is known automatically.
    """
    def __init__(self, expected_type: type):
        self.expected_type = expected_type
        self.storage_name = ""  # filled by __set_name__

    def __set_name__(self, owner, name):
        # Called at class creation time; records the attribute name
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self  # class-level access returns the descriptor
        return getattr(instance, self.storage_name, None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.storage_name.lstrip('_')} must be "
                f"{self.expected_type.__name__}, got {type(value).__name__}"
            )
        setattr(instance, self.storage_name, value)


class Employee:
    """Employee with type-checked attributes via descriptors."""
    name = Typed(str)
    salary = Typed((int, float))  # accepts int or float
    active = Typed(bool)

    def __init__(self, name: str, salary: float, active: bool = True):
        self.name = name
        self.salary = salary
        self.active = active

    def __repr__(self) -> str:
        return (f"Employee(name={self.name!r}, salary={self.salary}, "
                f"active={self.active})")


print("BONUS:   Typed descriptor")
e = Employee("Carlos", 45000.0, True)
print(f"  {e}")
assert e.name == "Carlos"
assert e.salary == 45000.0

# Type validation
try:
    e.name = 42  # should fail — name must be str
except TypeError as err:
    print(f"  Caught: {err}")

try:
    e.active = "yes"  # should fail — active must be bool
except TypeError as err:
    print(f"  Caught: {err}")

# Valid reassignment
e.salary = 52000.0
print(f"  Updated salary: {e.salary}")
assert e.salary == 52000.0

print("---")
print("✅ All Group 04 exercises passed!")
