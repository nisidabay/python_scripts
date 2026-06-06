#!/usr/bin/python3
import os
import subprocess


def get_process_info(process_name: str) -> None:
    """
    Prints detailed information about processes matching the given name.

    Args:
    process_name (str): The name of the process to search for.
    """
    try:
        # Using pgrep to find processes with the given name
        process_ids = (
            subprocess.check_output(["pgrep", "-f", process_name]).decode().split()
        )

        for pid in process_ids:
            print(f"Details for process ID {pid}:")
            # Printing process details
            os.system(f"ps u -p {pid}")
            # Printing the command line used to start the process
            os.system(f"cat /proc/{pid}/cmdline")
            print("\n")

    except subprocess.CalledProcessError:
        print(f"No processes found with the name '{process_name}'.")


get_process_info("firefox")
