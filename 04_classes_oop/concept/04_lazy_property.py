#!/usr/bin/python3
import math


class LazyProperty:
    """
    A decorator for creating lazy properties. The decorated method will only be
    called once and its result will be cached for future access.
    """

    def __init__(self, function):
        """
        Initialize the LazyProperty decorator.

        Args:
            function (callable): The method to be decorated.
        """
        self.function = function
        self.name = function.__name__

    def __get__(self, obj, type=None) -> object:
        """
        Get the value of the lazy property. If the value has not been calculated
        yet, calculate it using the decorated method and cache the result.

        Args:
            obj (object): The instance of the class.
            type (type): The class type.

        Returns:
            object: The computed or cached value of the lazy property.
        """
        if obj is None:
            return self

        if self.name not in obj.__dict__:
            obj.__dict__[self.name] = self.function(obj)
        return obj.__dict__[self.name]


class Circle:
    """
    A class representing a circle with a given radius.
    """

    def __init__(self, radius: float):
        """
        Initialize a Circle with the given radius.

        Args:
            radius (float): The radius of the circle.
        """
        self.radius = radius

    @LazyProperty
    def area(self) -> float:
        """
        Calculate and return the area of the circle.

        Returns:
            float: The area of the circle.
        """
        return math.pi * self.radius**2

    @LazyProperty
    def circumference(self) -> float:
        """
        Calculate and return the circumference of the circle.

        Returns:
            float: The circumference of the circle.
        """
        return 2 * math.pi * self.radius


# Create a Circle instance with a radius of 5
my_circle = Circle(5)

# Access the properties (calculations are done lazily)
print("Radius:", my_circle.radius)
print("Area:", my_circle.area)  # This triggers the area calculation.
print(
    "Circumference:", my_circle.circumference
)  # This triggers the circumference calculation.

# Access the properties again (cached results are used)
print("Area (again):", my_circle.area)  # Cached result.
print("Circumference (again):", my_circle.circumference)  # Cached result.
