#!/usr/bin/python3

import signal
##############################################################################
# Idea from: Internet
# Author:
# Description: Get all the OS valid signals
# Date:
# Dependencies:
##############################################################################

validsignls: set = signal.valid_signals()

print(validsignls)
