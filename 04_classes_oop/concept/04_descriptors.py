#!/usr/bin/python3
from random import choice, seed

# Seed the random number generator for reproducible results
seed(0)


class Deck1:
    """A class representing a deck of playing cards using property methods."""

    @property
    def suit(self) -> str:
        """
        Get a random suit from the deck.

        Returns:
            str: A random suit ("Spade", "Heart", "Diamond", or "Club").
        """
        return choice(("Spade", "Heart", "Diamond", "Club"))

    @property
    def card(self) -> str:
        """
        Get a random card from the deck.

        Returns:
            str: A random card ("2" to "10" or "J", "Q", "K", "A").
        """
        return choice(tuple("23456789JQKA") + ("10",))


d = Deck1()
for _ in range(10):
    print(d.card, d.suit)


class Choice:
    """A non-data descriptor class for making choices from a set of options."""

    def __init__(self, *choices: str) -> None:
        """
        Initialize a Choice descriptor with a set of choices.

        Args:
            *choices (str): The available choices.
        """
        self.choices = choices

    def __get__(self, instance, owner_class) -> str:
        """
        Get a random choice from the available choices.

        Args:
            instance: The instance of the class.
            owner_class: The class that owns this descriptor.

        Returns:
            str: A random choice from the available choices.
        """
        return choice(self.choices)


class Deck2:
    """A class representing a deck of playing cards using a descriptor."""

    suit = Choice("Spade", "Heart", "Diamond", "Club")
    card = Choice(*"23456789JQKA", "10")


d = Deck2()
for _ in range(10):
    print(d.suit, d.card)
