#!/usr/bin/python3
# Show the records. Never interact with the model
from model import Person


def showAllView(list: list):
    print(f"{len(list)} users in the database")

    for _ in list:
        print("f{Person.first_name}{Person.last_name}")


def starView():
    print("MVC - the simplest example")
    print("Do you want to see everyone in the database?[y/n]")


def endView():
    print("Goodbye")
