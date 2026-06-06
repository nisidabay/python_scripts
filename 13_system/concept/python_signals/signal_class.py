#!/usr/bin/python3
import signal
import time
from typing import Any


def signalHandler(signalnumb: int, frame: Any) -> None:
    print("Ctrl-C pressed")
    print("Exiting ...")
    exit(0)


def exitHandler(signalnumb: int, frame: Any) -> None:
    print("Ctrl-Z pressed")
    print("Exiting ...")
    exit(0)


signal.signal(signal.SIGINT, signalHandler)
signal.signal(signal.SIGTSTP, exitHandler)

while 1:
    time.sleep(3)
