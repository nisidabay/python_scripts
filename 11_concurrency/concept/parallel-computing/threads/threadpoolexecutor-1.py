#!/usr/bin/python3
##############################################################################
# Idea from: SuperFastPython.com
# Author:
# Modified by: Carlos Lacaci Moya
# Date: jue 24 nov 2022 12:45:29 CET

# Description: parallel for loop with ThreadPool Class

# We can create a pool of worker threads using the ThreadPoolExecutor class
# with a modern executor interface.
#
# This allows tasks to be issued as one-off tasks via the submit() method,
# returning Future object that provides a handle on the task. It also allows
# the same function to be called many times with different arguments via the
# map() method.
#
# THIS IS THE PREFERRED APPROACH FOR MODERN PARALLEL FOR-LOOPS.
##############################################################################

import concurrent.futures
from utilities.helpers import cpu_time, measure_execution


# execute a task
def task(value):
    """Return a result, if needed"""
    return value


@measure_execution
@cpu_time
def using_submit() -> None:
    """Issue some tasks and collect futures one at a time"""
    with concurrent.futures.ThreadPoolExecutor() as exe:
        # Creates 50 threads
        futures = [exe.submit(task, i) for i in range(50)]
        # Handle results as tasks are completed
        for future in concurrent.futures.as_completed(futures):
            if future.done():
                print(f">got {future.result()}")


@measure_execution
@cpu_time
def using_map() -> None:
    with concurrent.futures.ThreadPoolExecutor() as exe:
        """
        Issue one task for each call to the function
        return result in the order they were started
        """

        # Calling task 50 times
        for result in exe.map(task, range(50)):
            print(f">got {result}")


def main() -> None:
    """create the pool with the default number of workers"""

    using_submit()
    using_map()


if __name__ == "__main__":
    main()
