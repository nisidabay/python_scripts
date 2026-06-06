#!/usr/bin/env python3
# argparse_01: Boolean flags with store_true/store_false — a backup script
import argparse

parser = argparse.ArgumentParser(description="Backup tool — archive files to a target directory.")
parser.add_argument("--verbose", action="store_true", help="Enable detailed output")
parser.add_argument("--quiet",   action="store_true", help="Suppress all non-error output")
parser.add_argument("--dry-run", action="store_true", help="Show what would happen without doing it")
args = parser.parse_args()

if args.quiet:
    print("Backup running silently...")
elif args.verbose:
    print("Verbose mode: scanning files, checking timestamps, compressing...")
else:
    print("Backup: normal mode.")

if args.dry_run:
    print("DRY-RUN: no files will be modified.")

if __name__ == "__main__":
    pass  # argparse runs automatically above
