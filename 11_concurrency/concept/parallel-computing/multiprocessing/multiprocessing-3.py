#!/usr/bin/python3
"""
File:multi_example-1.py 
Author: James Cutajar
Modified by: Carlos Lacaci Moya
Github: https://www.udemy.com/course/parallel-computing-in-python/

Description: Using multiprocessing to spawn/fork several process
    Every process is independent, has its own memory, run in separate
    core and don't interfere with each other.

In this cases takes more time 'cause each core is performing one task
indepently
"""
import multiprocessing
import resource
from functools import wraps
from multiprocessing import Process
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
    num_cores = multiprocessing.cpu_count()

    i = 0
    # Every core performs the same operation, so it takes longer
    for c in range(num_cores):
        print(f"Using core {c} of {num_cores} core(s)")
        for _ in range(20_000_000):
            i += 1

    # Get the current CPU usage percent for the script process
    process = psutil.Process()
    cpu_percent = process.cpu_percent()
    print(f"CPU utilization: {cpu_percent}%")


def main():
    # Create a process object
    multiprocessing.set_start_method("fork")
    for _ in range(5):
        p = Process(target=do_work, args=())

        # Start the process
        p.start()

        # Wait for the process to complete
        p.join()


if __name__ == "__main__":
    main()
