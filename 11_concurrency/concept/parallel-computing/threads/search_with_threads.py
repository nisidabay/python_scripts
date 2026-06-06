#!/usr/bin/python3

from pathlib import Path
from utilities.helpers import measure_execution
from threading import Thread

matches = []


def file_search(root_folder: Path, filename: str) -> None:
    for file in root_folder.iterdir():
        full_path = file.joinpath(file)
        if filename in full_path.stem:
            matches.append(full_path)
        if full_path.is_dir():
            file_search(full_path, filename)


@measure_execution
def main() -> None:

    thread = Thread(target=file_search,
                    args=(Path("/home/nisidabay").resolve(), "README.md"))
    thread.start()
    thread.join()

    for m in matches:
        print(f"Matched: {m}")


if __name__ == "__main__":
    main()
