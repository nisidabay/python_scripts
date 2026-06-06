#!/usr/bin/python3


def permutate(string, pocket="-") -> str:
    together = ""
    permutation = ""
    if len(string) == 0:
        return pocket

    for i in range(len(string)):
        letter = string[i]
        print(f"{letter=}")
        front = string[:i]
        print(f"{front=}")
        back = string[i + 1:]
        print(f"{back=}")
        together = front + back
        print(f"{together=}")
        permutation += permutate(together, letter + pocket)

    return permutation


print(permutate("ABC").removesuffix("-"))
