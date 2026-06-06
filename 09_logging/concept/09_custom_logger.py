#!/usr/bin/python3
""" Custom logger """
# ------------------------------------------------------------------------------
# Name:        custom_logger_new.py
# Purpose:     Multipurpose logger
# Version:     Beta
# Date: dom 08 ago 2021 10:50:05 CEST
# Author:      clacmoy
# Idea from RealPython
# Modifications: Added dataclass
# The logger must be initialize ONCE an call everywhere
# ------------------------------------------------------------------------------
import logging
from dataclasses import dataclass


@dataclass
class CustomLogger:
    """ Customable logger """

    logfile_name: str
    FileHandler_level: str
    logger_name: str
    console_level: str
    console_enabled: bool = False

    def __post_init__(self):
        # Handlers
        self.file_handler = logging.FileHandler(self.logfile_name)
        self.console_handler = logging.StreamHandler()

        # Initialize logger
        self._set_logger()

    def _set_logger(self):
        """ Inialize logger """

        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel("INFO")

        # Set the formatters for the handlers
        console_format, file_format = self._set_formatters()

        if self.console_enabled:
            # Console_handler
            self.console_handler.setLevel(self.console_level)
            self.console_handler.setFormatter(console_format)

            # Add handler to the CustomLogger
            self.logger.addHandler(self.console_handler)

        # File_handler
        self.file_handler.setLevel(self.FileHandler_level)
        self.file_handler.setFormatter(file_format)

        # Add handler to the CustomLogger
        self.logger.addHandler(self.file_handler)

    def _set_formatters(self):
        """ Set the formatters """

        #console_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        console_format = CustomFormatter()

        file_format = logging.Formatter(
            "%(asctime)s  - %(name)s - %(levelname)s - On line: %(lineno)d - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
        )

        return console_format, file_format


class CustomFormatter(logging.Formatter):
    """ Colored Logging Formatter """

    grey = "\x1b[38;21m"
    green = "\x1b[32;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    message = "%(asctime)s - %(name)s - %(levelname)s -\
%(message)s (%(filename)s:%(lineno)d)"

    # Formats dictionary
    FORMATS = {
        logging.DEBUG: grey + message + reset,
        logging.INFO: green + message + reset,
        logging.WARNING: yellow + message + reset,
        logging.ERROR: red + message + reset,
        logging.CRITICAL: bold_red + message + reset
    }

    def format(self, record):
        print(f"RECORD IS {record}")
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


if __name__ == "__main__":
    log3 = CustomLogger("program.log", "INFO", "mi_error", "WARNING", True)
    log3.logger.warning("THIS IS A WARNING MESSAGE")
    log3.logger.info("THIS IS A INFO MESSAGE")
    print(log3)
