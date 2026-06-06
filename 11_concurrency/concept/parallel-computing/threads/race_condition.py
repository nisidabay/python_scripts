#!/usr/bin/python3
""" Simulate a race condition using threads 
This is due to not using .join() method
"""
from threading import Thread
from utilities.helpers import measure_execution


class StingySpendy():

    money = 100

    def stingy(self) -> None:
        """ Add money """
        for _ in range(1_000_000):
            self.money += 10

    def spendy(self) -> None:
        """ Retrives money """
        for _ in range(1_000_000):
            self.money -= 10


@measure_execution
def main() -> None:
    """ Runs the threads """
    ss = StingySpendy()
    t1 = Thread(target=ss.stingy, args=())
    t1.start()
    t2 = Thread(target=ss.spendy, args=())
    t2.start()

    print(f"Money in the end: {ss.money}")


if __name__ == "__main__":
    main()
