#!/usr/bin/python3
"""
You might want to subclass the Thread class if you need to customize the behavior 
of the thread in some way, such as setting custom instance variables or adding 
additional methods.
"""
import threading


class MyThread(threading.Thread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.message = "Hello, world!"

    def run(self):
        print(self.message)


thread = MyThread()
thread.start()
