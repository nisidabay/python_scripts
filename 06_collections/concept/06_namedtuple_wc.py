#!/usr/bin/python3
""" Count newlines, words and words of a text passed as argument 
Mimic wc command"""

from collections import namedtuple
import pathlib
import sys

counter = namedtuple("Counter", ["lines", "words", "chars"])
statistics = {}
for filename in sys.argv[1:]:
    path = pathlib.Path(filename)

    _counter = counter(
        path.read_text(encoding="utf-8").count("\n"),
        len(path.read_text(encoding="utf-8").split()),
        len(path.read_text(encoding="utf-8")),
    )

    statistics[filename] = _counter

for k, v in statistics.items():
    print(
        f"File name: {k}, Lines: {[v.lines]}, Words: {[v.words]}, Chars: {[v.chars]}"
    )
