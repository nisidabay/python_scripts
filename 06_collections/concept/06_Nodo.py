#!/usr/bin/python3
""" Listas anidadas """
from dataclasses import dataclass
from typing import Any


@dataclass
class Nodo:
    _value: int
    _next: Any = None

    def agregar(self, value):
        if self._next:
            next_value = self._next.agregar(value)
            print(f"Next node: {next_value}")

        else:
            self._next = Nodo(value)
            print(f"New node: {self._next}")

    def listar(self):
        if self._next:
            next_item = self._next.listar()
        else:
            return self._value
        return f"{self._value} -> {next_item}"


if __name__ == "__main__":
    lista = Nodo(5)
    lista.agregar(3)
    lista.agregar(4)
    lista.agregar(8)
    lista.agregar(2)
    print(lista.listar())
