#!/usr/bin/python3


from typing import Iterator


def transaction_id(tid: int) -> Iterator[int]:
    while True:
        tid += 1
        yield tid


class Account:
    transaction_counter = transaction_id(100)

    def make_transaction(self) -> int:
        return next(Account.transaction_counter)


if __name__ == "__main__":
    a1 = Account()
    a2 = Account()
    print(a1.make_transaction())
    print(a2.make_transaction())
    print(a1.make_transaction())
