"""
File:count-letters-1.py 
Author: James Cutajar
Modified by: Carlos Lacaci Moya 

Web: https://www.udemy.com/course/parallel-computing-in-python/

Description: Count letters from text files without threading
"""

import json
from string import ascii_lowercase
from typing import Final
import tabulate
import requests
from utilities.helpers import cpu_time, measure_execution

# Url from where to get data
URL: Final = "https://www.rfc-editor.org/rfc/"


def count_letters(url: str, frequency: dict[str, int]) -> None:
    """Store the frequency of letters in a dictionary"""
    response = requests.get(url)
    txt = response.text

    for l in txt:
        letter = l.lower()
        if letter in frequency:
            frequency[letter] += 1


@cpu_time
@measure_execution
def main():
    """Get the total of each letter from several texts in the web"""
    # Initialize the dictionary
    frequency = {c: 0 for c in ascii_lowercase}

    # Get 20 pages
    for counter in range(1000, 1020):
        count_letters(f"{URL}rfc{counter}.txt", frequency)

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
