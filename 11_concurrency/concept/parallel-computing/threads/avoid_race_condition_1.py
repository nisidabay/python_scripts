#!/usr/bin/python3

"""
File: avoid_race_condition_1.py
Author: James Cutajar
Modified by: Carlos Lacaci Moya 

Web: https://www.udemy.com/course/parallel-computing-in-python/

    Avoid race condition by using .Lock() method 
    With .join() method  there is no need of using threadin.Lock()
"""
from threading import Thread, Lock
from utilities.helpers import measure_execution, cpu_time


class StingySpendy:
    """Fake class to simulate race conditions"""

    # Class Variable
    money = 100
    lock = Lock()

    def stingy(self) -> None:
        """Add money"""
        print("Adding money")
        for _ in range(1_000_000):
            with self.lock:
                self.money += 10

    def spendy(self) -> None:
        """Retrieves money"""
        print("Retrieving money")
        for _ in range(1_000_000):
            with self.lock:
                self.money -= 10


@cpu_time
@measure_execution
def main() -> None:
    """Run the threads"""
    ss = StingySpendy()

    thread1 = [Thread(target=ss.stingy, args=()) for _ in range(5)]
    thread2 = [Thread(target=ss.spendy, args=()) for _ in range(5)]
    threads_pool = [thread1, thread2]

    for t in threads_pool:
        for thread in t:
            thread.start()

    for t in threads_pool:
        for thread in t:
            thread.join()

    print(f"\nMoney in the end: {ss.money}")


if __name__ == "__main__":
    main()
