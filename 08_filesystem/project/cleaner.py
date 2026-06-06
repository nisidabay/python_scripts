#!/usr/bin/env python3
"""Disk usage analyzer — walks a directory, groups by extension, reports top 10 largest, can archive old files."""

import argparse
import os
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timedelta


def get_size_str(size_bytes: int) -> str:
    """Human-readable size."""
    s = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if s < 1024:
            return f"{s:.1f} {unit}"
        s /= 1024
    return f"{s:.1f} PB"


def walk_directory(root: Path) -> dict:
    """Walk *root* and return {ext: [paths]}."""
    by_ext = defaultdict(list)
    for entry in root.rglob("*"):
        if entry.is_file():
            ext = entry.suffix.lower() or "(no extension)"
            by_ext[ext].append(entry)
    return by_ext


def cmd_report(args) -> int:
    root = Path(args.dir).resolve()
    if not root.is_dir():
        print(f"Error: '{root}' is not a directory.", file=sys.stderr)
        return 1

    by_ext = walk_directory(root)

    # Build per-extension stats
    stats = []
    for ext, files in by_ext.items():
        total = sum(f.stat().st_size for f in files)
        stats.append((ext, len(files), total))

    stats.sort(key=lambda x: x[2], reverse=True)

    print(f"\nDisk usage report for: {root}")
    print(f"{'Extension':<16} {'Files':>8} {'Total Size':>14}")
    print("-" * 40)
    for ext, count, size in stats[:min(args.top, len(stats))]:
        print(f"{ext:<16} {count:>8} {get_size_str(size):>14}")
    print("-" * 40)
    total_files = sum(s[1] for s in stats)
    total_size = sum(s[2] for s in stats)
    print(f"{'TOTAL':<16} {total_files:>8} {get_size_str(total_size):>14}")
    return 0


def cmd_archive(args) -> int:
    root = Path(args.dir).resolve()
    dest = Path(args.dest).resolve()
    days = args.older_than

    if not root.is_dir():
        print(f"Error: '{root}' is not a directory.", file=sys.stderr)
        return 1

    dest.mkdir(parents=True, exist_ok=True)

    cutoff = datetime.now() - timedelta(days=days)
    moved = 0

    for entry in root.rglob("*"):
        if entry.is_file():
            mtime = datetime.fromtimestamp(entry.stat().st_mtime)
            if mtime < cutoff:
                rel = entry.relative_to(root)
                target = dest / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.move(str(entry), str(target))
                    moved += 1
                except OSError as exc:
                    print(f"Warning: could not move {entry}: {exc}", file=sys.stderr)

    print(f"Archived {moved} file(s) older than {days} day(s) into {dest}")
    return 0


def cmd_top(args) -> int:
    root = Path(args.dir).resolve()
    if not root.is_dir():
        print(f"Error: '{root}' is not a directory.", file=sys.stderr)
        return 1

    files = [(f, f.stat().st_size) for f in root.rglob("*") if f.is_file()]
    files.sort(key=lambda x: x[1], reverse=True)

    print(f"\nLargest {min(args.top, len(files))} file(s) in: {root}")
    print(f"{'Size':>14}  Path")
    print("-" * 60)
    for f, size in files[: args.top]:
        print(f"{get_size_str(size):>14}  {f}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Disk usage analyzer — report, list largest files, or archive old files.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # report
    p_report = sub.add_parser("report", help="Show disk usage grouped by extension")
    p_report.add_argument("dir", nargs="?", default=".", help="Directory to analyze (default: .)")
    p_report.add_argument("--top", type=int, default=10, help="Number of extensions to show (default: 10)")

    # top
    p_top = sub.add_parser("top", help="List the largest files")
    p_top.add_argument("dir", nargs="?", default=".", help="Directory to analyze (default: .)")
    p_top.add_argument("--top", type=int, default=10, help="Number of files to show (default: 10)")

    # archive
    p_archive = sub.add_parser("archive", help="Move old files to an archive directory")
    p_archive.add_argument("dir", help="Source directory")
    p_archive.add_argument("dest", help="Archive destination directory")
    p_archive.add_argument("--older-than", type=int, default=90, metavar="DAYS",
                           help="Move files older than DAYS days (default: 90)")

    args = parser.parse_args()

    if args.command == "report":
        return cmd_report(args)
    elif args.command == "top":
        return cmd_top(args)
    elif args.command == "archive":
        return cmd_archive(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
