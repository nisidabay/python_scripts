#!/usr/bin/python3
##############################################################################
# Idea from: SuperFastPython.com
# Author:
# Description: parallel for loop with Thread
# Date: jue 24 nov 2022 12:45:29 CET

# We can create a new thread for each iteration of the loop.
# This can be achieved by creating a Thread object and setting the target argument
# to the name of the function to execute and pass any arguments via the args
# argument.

# We can create all the required threads first using a list comprehension. Once
# created, all of the threads can be started at once by calling the start() method
# on each. Finally, we can wait for all the threads to finish by joining each in
# turn with the join() method.

# It is less effective if we have many more tasks than we can support concurrently
# because all of the tasks will run at the same time and could slow each other down.
# It also does not allow results from tasks to be returned easily.
##############################################################################

from threading import Thread
from utilities.helpers import cpu_time, measure_execution


class ParallelThread:
    def __init__(self):
        self.threads = []

    def create_tasks(self):
        self.threads = [Thread(target=self.task, args=(i,)) for i in range(20)]

    def start_threads(self):
        for thread in self.threads:
            thread.start()

    @cpu_time
    @measure_execution
    def wait_to_complete(self):
        for thread in self.threads:
            thread.join()
        print("Finished!")

    @staticmethod
    def task(value):
        print("*" * value)


if __name__ == "__main__":
    p = ParallelThread()
    p.create_tasks()
    p.start_threads()
    p.wait_to_complete()
