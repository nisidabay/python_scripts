#!/usr/bin/python
#
# Show file statistics by extension.

import os
import sys
from typing import Dict, List, Optional


class FileStats:
    """
    Show file statistics by extension.
    """

    def __init__(self) -> None:
        """
        Initialize the FileStats object.
        """
        self.stats: Dict[str, Dict[str, int]] = {}

    def statargs(self, args: List[str]) -> None:
        """
        Process the list of arguments and gather statistics for each file/directory.

        Args:
            args (List[str]): A list of file/directory paths.

        """
        for arg in args:
            if os.path.isdir(arg):
                self.statdir(arg)
            elif os.path.isfile(arg):
                self.statfile(arg)
            else:
                sys.stderr.write(f"Can't find {arg}\n")
                self.addstats("<???>", "unknown", 1)

    def statdir(self, dir_path: str) -> None:
        """
        Gather statistics for a directory and its contents.

        Args:
            dir_path (str): Path to the directory.

        """
        self.addstats("<dir>", "dirs", 1)
        try:
            names = os.listdir(dir_path)
        except OSError as err:
            sys.stderr.write(f"Can't list {dir_path}: {err}\n")
            self.addstats("<dir>", "unlistable", 1)
            return
        for name in sorted(names):
            # if name.startswith(".#"):
            #     continue  # Skip CVS temp files
            # if name.endswith("~"):
            #     continue  # Skip Emacs backup files
            full_path = os.path.join(dir_path, name)
            if os.path.islink(full_path):
                self.addstats("<lnk>", "links", 1)
            elif os.path.isdir(full_path):
                self.statdir(full_path)
            else:
                self.statfile(full_path)

    def statfile(self, file_path: str) -> None:
        """
        Gather statistics for a single file.

        Args:
            file_path (str): Path to the file.

        """
        head, ext = os.path.splitext(file_path)
        head, base = os.path.split(file_path)
        if ext == base:
            ext = ""  # E.g. .cvsignore is deemed not to have an extension
        ext = os.path.normcase(ext) or "<none>"
        self.addstats(ext, "files", 1)
        try:
            with open(file_path, "rb") as f:
                data = f.read()
        except IOError as err:
            sys.stderr.write(f"Can't open {file_path}: {err}\n")
            self.addstats(ext, "unopenable", 1)
            return
        self.addstats(ext, "bytes", len(data))
        if b"\0" in data:
            self.addstats(ext, "binary", 1)
            return
        if not data:
            self.addstats(ext, "empty", 1)
        lines = str(data, "latin-1").splitlines()
        self.addstats(ext, "lines", len(lines))
        del lines
        words = data.split()
        self.addstats(ext, "words", len(words))

    def addstats(self, ext: str, key: str, n: int) -> None:
        """
        Add statistics for a specific extension and key.

        Args:
            ext (str): File extension.
            key (str): Type of statistics (e.g., "files", "dirs", "bytes").
            n (int): Number of occurrences for the given extension and key.

        """
        d: Dict[str, int] = self.stats.setdefault(ext, {})
        d[key] = d.get(key, 0) + n

    def report(self) -> None:
        """
        Display the file statistics in a tabular format.
        """
        exts = sorted(self.stats)
        # Get the column keys
        columns = {}
        for ext in exts:
            columns.update(self.stats[ext])
        cols = sorted(columns)
        colwidth = {}
        colwidth["ext"] = max(map(len, exts))
        minwidth = 6
        self.stats["TOTAL"] = {}
        for col in cols:
            total: int = 0
            cw = max(minwidth, len(col))
            for ext in exts:
                value: Optional[int] = self.stats[ext].get(col)
                if value is None:
                    w: int = 0
                else:
                    w = len(str(value))
                    total += value
                cw = max(cw, w)
            cw = max(cw, len(str(total)))
            colwidth[col] = cw
            self.stats["TOTAL"][col] = total
        exts.append("TOTAL")
        for ext in exts:
            self.stats[ext]["ext"] = ext
        cols.insert(0, "ext")

        def printheader() -> None:
            for col in cols:
                print("%*s" % (colwidth[col], col), end=" ")
            print()

        printheader()
        for ext in exts:
            for col in cols:
                value: Optional[int] = self.stats[ext].get(col, "")
                print("%*s" % (colwidth[col], value), end=" ")
            print()
        printheader()  # Another header at the bottom


def main() -> None:
    """
    Main function to execute the file statistics program.
    """
    args = sys.argv[1:] or [os.curdir]
    stats = FileStats()
    stats.statargs(args)
    stats.report()


if __name__ == "__main__":
    main()
