#!/usr/bin/python3
#------------------------------------------------------------------------------
# Name:        filehandler_logger.py
# Purpose:     Basic logger
# Author:      clacmoy
#------------------------------------------------------------------------------
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - ln: %(lineno)s - %(message)s"

logging.basicConfig(
    filename="uto3.log",
    level=logging.INFO,
    format=LOG_FORMAT,
    filemode="a",
)
logger = logging.getLogger("ted")
