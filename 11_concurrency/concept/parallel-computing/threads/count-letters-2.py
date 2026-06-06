"""
File:count-letters-1.py 
Author: James Cutajar
Email: 
Github: https://www.udemy.com/course/parallel-computing-in-python/

Description: Count letters from text files using threading
"""

import json
from string import ascii_lowercase
from threading import Thread
from typing import Final

import requests
import tabulate
from utilities.helpers import measure_execution, cpu_time

# Url from where to get date
URL: Final = "https://www.rfc-editor.org/rfc/"


def count_letters(url, frequency) -> None:
    """Store the frequency of letters in a dictionary"""
    response = requests.get(url)
    txt = response.text

    for l in txt:
        letter = l.lower()
        if letter in frequency:
            frequency[letter] += 1


@cpu_time
@measure_execution
def main() -> None:
    """Get the total of each letter from several text in the web"""
    # Initialize the dictionary
    frequency = {c: 0 for c in ascii_lowercase}

    # Store the threads
    threads = []

    for counter in range(1000, 1020):
        thread = Thread(
            target=count_letters, args=(f"{URL}rfc{counter}.txt", frequency)
        )
        threads.append(thread)
        thread.start()

    # Wait for all the threads to finished
    for thread in threads:
        thread.join()

    # Display the data
    json_data = json.dumps(frequency)
    # Print the table
    data = json.loads(json_data)
    print(
        tabulate.tabulate(
            data.items(), headers=["Letter", "Frequency"], tablefmt="fancy_grid"
        )
    )


if __name__ == "__main__":
    main()
