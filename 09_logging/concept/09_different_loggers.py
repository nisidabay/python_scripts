import logging

# Create logger1
logger1 = logging.getLogger("logger1")
logger1.setLevel(logging.DEBUG)

# Create logger2
logger2 = logging.getLogger("logger2")
logger2.setLevel(logging.WARNING)

# Create console handler for logger1
console_handler1 = logging.StreamHandler()
console_handler1.setLevel(logging.DEBUG)
console_handler1.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger1.addHandler(console_handler1)

# Create file handler for logger2
file_handler2 = logging.FileHandler("logger2.log")
file_handler2.setLevel(logging.WARNING)
file_handler2.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger2.addHandler(file_handler2)

# Log messages using the loggers
logger1.debug("Debug message from logger1")
logger1.info("Info message from logger1")
logger2.warning("Warning message from logger2")
logger2.error("Error message from logger2")
