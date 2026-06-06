#!/usr/bin/python3
##############################################################################
# Idea from: SuperFastPython.com
# Author:
# Description: parallel for loop with ThreadPool Class
# Date: jue 24 nov 2022 12:45:29 CET

# We can create a pool of worker threads that can be reused for many tasks.
# This can be achieved using the ThreadPool class that will create one worker
# for each logical CPU core in the system.

# The ThreadPool class can be created using the context manager interface,
# which ensures that it is closed and all workers are released once we are
# finished with it.

# We can call the same function many times with different arguments using the
# map() method on the ThreadPool class. Each call to the target function will
# be issued as a separate task.

# This approach is very effective for executing tasks that involve calling the
# same function many times with different arguments.

# The ThreadPool class provides many variations of the map() function, such as
# lazy versions and a version that allows multiple arguments to the task
# function.
##############################################################################

from multiprocessing.pool import ThreadPool


class ThreadPool1:
    def __init__(self):

        # create the pool with the default number of workers
        with ThreadPool() as pool:
            # issue one task for each call to the function
            for result in pool.map(self.task, range(100)):
                # handle the result
                print(f">got {result}")

            # report that all tasks are completed
            print("Done")

    # execute a task
    @staticmethod
    def task(value):
        print("*" * value)
        # ...
        # return a result, if needed
        return value


if __name__ == "__main__":
    ThreadPool1()
