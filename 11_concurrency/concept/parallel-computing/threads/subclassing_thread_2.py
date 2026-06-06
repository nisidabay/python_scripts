#!/usr/bin/python3
"""
Knowing if the thread is alive
"""
import threading
import time


class MyThread(threading.Thread):
    def run(self):
        time.sleep(2)
        return


if __name__ == "__main__":
    for _ in range(3):
        t = MyThread()
        t.start()
        print("This task has begun")
        print("t.is_alive()= ", t.is_alive())
        t.join()
        print("This task has finished")
        print("t.is_alive()= ", t.is_alive())
        print()
