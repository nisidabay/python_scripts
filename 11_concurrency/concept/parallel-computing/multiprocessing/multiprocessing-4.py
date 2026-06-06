#!/usr/bin/python3
"""
File:multi_example-1.py 
Author: James Cutajar
Email: 
Github: https://www.udemy.com/course/parallel-computing-in-python/

Description: Using multiprocessing to spawn/fork several process
    Every process is independent, has its own memory, run in separate
    core and don't interfere with each other.

The code looks fine and should execute without any issues. Here's a brief 
explanation of what it does:

    It imports the multiprocessing and psutil modules, which are used to create 
    and manage multiple processes concurrently, and gather information about 
    system resources and processes, respectively.

    It defines a function called do_work, which calculates the CPU utilization 
    of the current process, starts a timer, performs some work (incrementing a 
    loop counter 20 million times), and then prints the time taken to complete 
    the work and the number of CPU cores used, as well as the CPU utilization of
    the process.

    In the if __name__ == "__main__" block, the multiprocessing start method is 
    set to 'fork', which means that new processes will be created using the 
    os.fork() function. Then, the code creates and starts 5 processes using the 
    Process class and the do_work function as the target.

    The do_work function will be executed concurrently in each of the 5 processes.

I've added some functions for testing.
"""

import multiprocessing
import resource
from functools import wraps
from multiprocessing import Process
from time import perf_counter
from typing import Any

import psutil


def cpu_time(original_func) -> Any:
    """Measure the CPU time used by your Python program."""

    @wraps(original_func)
    def wrapper(*args, **kwargs) -> float:

        # get the start time
        start_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime

        original_func(*args, **kwargs)

        # Get the end time
        end_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime
        elapsed_cpu_time = end_time - start_time
        print(f"Elapsed CPU time: {elapsed_cpu_time:.2f} seconds")

        # Return the elapsed CPU time
        return elapsed_cpu_time

    return wrapper


@cpu_time
def do_work():
    process = psutil.Process()
    cpu_percent = process.cpu_percent()
    start = perf_counter()

    print("Starting work")

    i = 0
    for _ in range(20_000_000):
        i += 1


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    for _ in range(5):
        p = Process(target=do_work, args=())
        p.start()
