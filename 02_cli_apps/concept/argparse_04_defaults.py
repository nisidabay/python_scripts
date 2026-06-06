#!/usr/bin/env python3
# argparse_04: default=, const=, nargs='?' with const, set_defaults — a log viewer
import argparse

parser = argparse.ArgumentParser(description="View and filter application logs.")
parser.add_argument("--lines", type=int, default=50, help="Number of lines to show")

# nargs='?' makes the argument optional; const provides the value when flag is given without value
parser.add_argument("--tail", nargs="?", const=10, type=int, default=None,
                    help="Tail the last N lines (default 10 if used without a number)")

parser.add_argument("--level", nargs="?", const="WARN", default="INFO",
                    help="Minimum log level (INFO, WARN, ERROR); defaults to INFO, const=WARN if bare")

# set_defaults() attaches extra attributes that aren't tied to a specific argument
parser.set_defaults(max_file_size_mb=500)

args = parser.parse_args()

tail_info = f"tail last {args.tail} lines" if args.tail else "show from beginning"
print(f"Showing {args.lines} lines of logs, {tail_info}, level >= {args.level}")
print(f"Max log file size: {args.max_file_size_mb} MB")


if __name__ == "__main__":
    pass
