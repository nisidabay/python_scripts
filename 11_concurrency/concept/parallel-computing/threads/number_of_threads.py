#!/usr/bin/python3
"""
File: number_of_threads.py 
Author: ChatGPT
Email: 
Web: https://openai.com/
Description: 
    Show the number of threads available on your computer

In this example, the Semaphore class is used to create a semaphore with a 
initial value of 0. This causes any threads that try to acquire the semaphore 
to block indefinitely. The while loop then creates a new thread and starts it,
incrementing the max_threads counter each time. If an exception is raised when 
trying to start a new thread, it means that the maximum number of threads has 
been reached, and the loop breaks. The final value of max_threads is then 
printed to the console.

Note that the actual maximum number of threads that can be used in a Python 
program will depend on various factors, including the hardware and operating 
system being used. This example is just one way to determine the maximum number 
of threads that can be used in a Python program.
"""

import threading
from utilities.helpers import measure_execution, cpu_time


def thread_test():
    semaphore = threading.Semaphore(0)
    semaphore.acquire()


@measure_execution
@cpu_time
def maximum_threads() -> None:
    max_threads = 0
    while True:
        try:
            t = threading.Thread(target=thread_test)
            t.start()
            max_threads += 1
        except RuntimeError:
            print("Can't create more threads!")
            break
        # DEBUG
        # print(f"Threads created so far: {max_threads}")
    print(f"Maximum number of threads: {max_threads}")


if __name__ == "__main__":
    maximum_threads()
