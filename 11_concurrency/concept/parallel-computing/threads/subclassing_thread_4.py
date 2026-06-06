#!/usr/bin/python3
""" Passing arguments to a thread """
import threading
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s')


class MyThread(threading.Thread):
    def __init__(self, args=None, kwargs=None):
        super().__init__()

        self.args = args
        self.kwargs = kwargs

    def run(self):
        logging.debug('running with %s and %s', self.args, self.kwargs)
        time.sleep(.5)
        return


if __name__ == "__main__":
    for i in range(3):
        t = MyThread(args=i, kwargs={'a': 1, 'b': 2})
        t.start()
        t.join()
