#!/usr/bin/python3
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def __str__(self):
        return f"Dog: {self.name}\tBreed: {self.breed}"


class Person:
    def __init__(self, name, dni):
        self.name = name
        self.dni = dni

    def __str__(self):
        return f"Person: {self.name}\tDNI: {self.dni}"


class Client(Person):
    def __init__(self, name, dni, dog_name, dog_breed):
        super().__init__(name, dni)

        # Composition
        self.dog = Dog(dog_name, dog_breed)

    # Method overriding
    def __str__(self):
        return f"{super().__str__()}\n{self.dog}"


c = Client(name="Carlos", dni="111", dog_name="Chucho", dog_breed="Dalmatian")
print(c)
