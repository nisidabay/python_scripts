#!/usr/bin/python3
"""
Show if a thred is alive using logging
"""
import threading
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s')


class MyThread(threading.Thread):
    def run(self):
        logging.debug('running')
        time.sleep(.5)
        logging.debug(f"Thread is alive?: {self.is_alive()}")


if __name__ == "__main__":
    for _ in range(3):
        t = MyThread()
        t.start()
        logging.debug(f"Thread is alive?: {t.is_alive()}")
        t.join()
        logging.debug(f"Thread is alive?: {t.is_alive()}")
