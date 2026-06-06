#!/usr/bin/python3
import signal
import time
from typing import Any

##############################################################################
# Idea from: Internet
# Author:
# Description: Example of SIGINT and SIGTSTP signals
# Date:
# Dependencies:
##############################################################################


def signalHandler(signalnumb: int, frame: Any) -> None:
    print("Signal Number:", signalnumb, " Frame: ", frame)


def exitHandler(signalnumb: int, frame: Any) -> None:
    print("Signal Number:", signalnumb, " Frame: ", frame)
    print('Exiting!!!!')
    exit(0)


# With 'SIGINT' (CTRL + C), we can register our signal handler.
signal.signal(signal.SIGINT, signalHandler)

# 'SIGTSTP' (Ctrl + Z) is used to register the exit handler.
signal.signal(signal.SIGTSTP, exitHandler)

while 1:
    # print the text ctrl+c
    print("Please Press Ctrl + C")
    # sleep for 3 seconds using the sleep() function in time
    time.sleep(3)
