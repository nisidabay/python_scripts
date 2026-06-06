# Classes & OOP — classmethod, composition, factory, methods, properties, descriptors, singleton, multiple constructors

## Quick Start
```bash
python 04_classmethod.py
python 04_composition.py
python 04_factory.py
python 04_methods_runtime.py
python 04_getters_setters.py
python 04_lazy_property.py
python 04_descriptors.py
python 04_singleton.py
python multiple_constructors/demo_multiple_constructors.py
python multiple_constructors/circle.py
python multiple_constructors/person.py
python multiple_constructors/point.py
python multiple_constructors/power.py
python multiple_constructors/callable_objects.py
python multiple_constructors/multiple_constructors.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `04_classmethod.py` | Alternative constructor via `@classmethod` | `cls(x)` returns new instance, `from_string(cls, s)` factory |
| `04_composition.py` | "Has-a" over "Is-a" | `self.dog = Dog(name, breed)`, delegation to composed object |
| `04_factory.py` | Factory pattern with abstract base class | `ABC`, `@abstractmethod`, `TaxCalculatorFactory.create(...)` |
| `04_methods_runtime.py` | Monkey-patch methods at runtime | `MethodType(func, self)`, `setattr`, `getattr` with default |
| `04_getters_setters.py` | `@property` with validation | `@property` + `@age.setter`, validation in setter |
| `04_lazy_property.py` | Compute-once descriptor | Custom `LazyProperty` descriptor, `obj.__dict__[self.name] = ...` |
| `04_descriptors.py` | Non-data descriptor for random picks | `Choice.__get__`, `Deck2.suit = Choice("Spade","Heart",...)` |
| `04_singleton.py` | Single instance pattern | `_instance = None`, `@staticmethod get_instance()` |
| `multiple_constructors/circle.py` | `@classmethod` as alt constructor | `Circle.from_diameter(diameter)`, `cls(radius=diameter//2)` |
| `multiple_constructors/person.py` | `singledispatchmethod` on `__init__` | `@singledispatchmethod`, type-based dispatch for `date`/`str`/`int`/`float` |
| `multiple_constructors/point.py` | Cartesian→polar conversion constructor | `PolarPoint.from_cartesian(x, y)`, `math.atan2` |
| `multiple_constructors/callable_objects.py` | `__call__` makes instances callable | `self.total += base**self._exponent`, accumulating state |
| `multiple_constructors/power.py` | Callable factory with accumulator | Same pattern as callable_objects — class with `__call__` |
| `multiple_constructors/multiple_constructors.py` | `singledispatchmethod` on methods | `@singledispatchmethod`, `@generic_method.register(int)` |
| `multiple_constructors/demo_multiple_constructors.py` | Demo of singledispatch | Multiple registered implementations by argument type |

## Common Patterns
```python
from functools import singledispatchmethod
from abc import ABC, abstractmethod
from types import MethodType

# Alternative constructor with @classmethod
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @classmethod
    def from_diameter(cls, diameter):
        return cls(radius=diameter / 2)

# Composition over inheritance
class Client:
    def __init__(self, name, dog_name):
        self.dog = Dog(dog_name)          # has-a, not is-a

# Factory pattern
class TaxCalculatorFactory:
    def create(self, tax_type: str) -> TaxCalculator:
        if tax_type == "standard":
            return StandardTaxCalculator()
        raise ValueError(f"Unknown: {tax_type}")

# Property with validation
class Age:
    def __init__(self, age):
        self.age = age                    # calls setter

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise ValueError("Must be int")
        self._age = value

# Lazy property (compute once, cache forever)
class LazyProperty:
    def __get__(self, obj, type=None):
        if obj is None:
            return self
        if self.name not in obj.__dict__:
            obj.__dict__[self.name] = self.function(obj)
        return obj.__dict__[self.name]

# Singleton
class Singleton:
    _instance = None
    @staticmethod
    def get_instance():
        if Singleton._instance is None:
            Singleton._instance = Singleton()
        return Singleton._instance

# singledispatchmethod — type-based dispatch
class BirthInfo:
    @singledispatchmethod
    def __init__(self, birth_date):
        raise ValueError(f"Unsupported: {birth_date}")

    @__init__.register(str)
    def _from_str(self, birth_date):
        self.date = date.fromisoformat(birth_date)
```

## Now Build Your Own
Build a `BankAccount` system:
1. `BankAccount` with `@property` for balance — setter validates non-negative.
2. `@classmethod from_json(cls, path)` — loads account from a JSON file.
3. `SavingsAccount` using **composition** with an `InterestCalculator` object (not inheritance).
4. A `LazyProperty` descriptor `monthly_interest` that computes `balance * rate / 12` once.
5. A `AccountFactory` that returns `BankAccount` or `SavingsAccount` based on a `type` string.
6. A `TransactionLogger` **singleton** shared across all accounts.
