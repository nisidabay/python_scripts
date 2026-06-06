#!/usr/bin/python3

# Model
# Consists of pure application logic. Interact with the database.

import json
from dataclasses import dataclass


@dataclass
class Person:
    """ Generate Person objects from json file """
    first_name: str = ""
    last_name: str = ""

    def __repr__(self):
        return f"Person(first_name={self.first_name},last_name={self.last_name})"

    @classmethod
    def create(cls):
        """ Create Persons """
        result = []
        with open("db.json") as data:
            json_list = json.load(data)

            for item in json_list["Persons"]:
                # Create Persons objects
                person = cls(item["first_name"], item["last_name"])
                result.append(person)
            return result


if __name__ == "__main__":
    p = Person()
    people = p.create()
    print(people)
