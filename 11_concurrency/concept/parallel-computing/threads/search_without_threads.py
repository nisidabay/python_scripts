#!/usr/bin/python3
""" Search a file without using threads """

from pathlib import Path
from utilities.helpers import measure_execution

matches = []


def file_search(root_folder: Path, filename: str) -> None:
    """ Search for a file recursively """

    for file in root_folder.iterdir():
        full_path = file.joinpath(file)
        if filename in full_path.stem:
            matches.append(full_path)
        if full_path.is_dir():
            file_search(full_path, filename)


@measure_execution
def main() -> None:
    """ Execute the search """

    file_search(Path("/home/nisidabay").resolve(), "README.md")

    if matches:
        for m in matches:
            print(f"Matched: {m}")
    else:
        print("No matches found")


if __name__ == "__main__":
    main()
