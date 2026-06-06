#!/usr/bin/env python3
"""Log file processor: streams large files with generators, filters with generator expressions, chains iterators.

Uses only stdlib — generators, itertools, context managers for file handling.
"""

from __future__ import annotations

import argparse
import itertools
import re
import sys
from pathlib import Path
from typing import Iterator, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------
def read_lines(path: Path, encoding: str = "utf-8") -> Iterator[str]:
    """Yield lines from a file lazily (memory-efficient streaming)."""
    with open(path, encoding=encoding) as f:
        yield from f


def parse_nginx(lines: Iterator[str]) -> Iterator[Tuple[str, str, str, str, str]]:
    """Parse nginx/access-log lines into (ip, date, method, path, status) tuples.

    Example: 127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200
    """
    pattern = re.compile(
        r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) \S+" (\d+)'
    )
    for line in lines:
        m = pattern.search(line)
        if m:
            yield (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))


def parse_generic(lines: Iterator[str]) -> Iterator[Tuple[int, str]]:
    """Yield (lineno, stripped_line) lazily — generic log parser."""
    for i, line in enumerate(lines, 1):
        stripped = line.rstrip("\n").rstrip("\r")
        if stripped:
            yield (i, stripped)


# ---------------------------------------------------------------------------
# Filter pipelines (generator expressions)
# ---------------------------------------------------------------------------
def status_filter(entries: Iterator[Tuple[str, str, str, str, str]], code: str) -> Iterator:
    """Filter entries by HTTP status code."""
    return (e for e in entries if e[4] == code)


def method_filter(entries: Iterator[Tuple[str, str, str, str, str]], method: str) -> Iterator:
    """Filter entries by HTTP method."""
    return (e for e in entries if e[3].upper() == method.upper())


def grep_filter(lines: Iterator[Tuple[int, str]], pattern: str) -> Iterator:
    """Filter lines matching a regex pattern."""
    regex = re.compile(pattern)
    return ((n, line) for n, line in lines if regex.search(line))


# ---------------------------------------------------------------------------
# Iterator chaining (itertools)
# ---------------------------------------------------------------------------
def chain_sources(paths: List[Path]) -> Iterator[str]:
    """Chain multiple log files into a single line stream."""
    iterators = [read_lines(p) for p in paths]
    return itertools.chain.from_iterable(iterators)


def top_n(items: Iterator, n: int, key_func=None):
    """Return top N items from a stream using heapq internally
    (demonstrates passing generators to consuming functions)."""
    import heapq
    return heapq.nlargest(n, items, key=key_func)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Stream and filter log files using generators — memory-efficient."
    )
    p.add_argument("files", nargs="+", type=Path, help="Log files to process")
    p.add_argument("--format", choices=("generic", "nginx"), default="generic",
                   help="Log format (default: generic)")
    p.add_argument("--grep", type=str, help="Regex filter on line content")
    p.add_argument("--status", type=str, help="Filter by HTTP status code (nginx format)")
    p.add_argument("--method", type=str, help="Filter by HTTP method (nginx format)")
    p.add_argument("--limit", type=int, default=0, help="Limit output to first N entries")
    p.add_argument("--count", action="store_true", help="Only show match count, not content")
    return p


def main() -> None:
    args = build_parser().parse_args()

    # Build the iterator pipeline
    lines: Iterator = chain_sources(args.files)

    if args.format == "nginx":
        entries: Iterator = parse_nginx(lines)
        if args.method:
            entries = method_filter(entries, args.method)
        if args.status:
            entries = status_filter(entries, args.status)

        if args.count:
            count = sum(1 for _ in entries)
            print(f"{count} matching entries")
            return

        if args.limit:
            entries = itertools.islice(entries, args.limit)

        # Format output
        for ip, date, method, path, status in entries:
            print(f"{ip:15s}  {date:28s}  {method:6s}  {path:40s}  {status}")

    else:
        # Generic pipeline
        parsed: Iterator = parse_generic(lines)

        if args.grep:
            parsed = grep_filter(parsed, args.grep)

        if args.count:
            count = sum(1 for _ in parsed)
            print(f"{count} matching lines")
            return

        if args.limit:
            parsed = itertools.islice(parsed, args.limit)

        for lineno, line in parsed:
            print(f"{lineno:6d}: {line}")


if __name__ == "__main__":
    main()
