#!/usr/bin/python3
import signal
import time
from typing import Any

##############################################################################
# Idea from: Internet
# Author:
# Description: Example of alarm signal
# Date:
# Dependencies:
##############################################################################


def alarmhandler(signalnumb: int, frame: Any) -> None:
    """ This will be triggered by the signal.alarm"""
    print('The Alarm Time is:', time.ctime())


# Initiate our handler of the alarm signal
signal.signal(signal.SIGALRM, alarmhandler)

# After 3 seconds, set the alarm.
signal.alarm(3)

print('The current Time is:', time.ctime())
# sleep for 3 seconds using the sleep() function in time
time.sleep(3)
