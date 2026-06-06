#!/usr/bin/env python3
# argparse_08: Help formatting — formatter_class, epilog, defaults in help — a release manager
import argparse

EPILOG = """
Examples:
  release --version 2.3.0 --dry-run          Preview a release
  release --version 2.3.0 --repo backend     Tag backend only
  release --version 2.3.0 --notes CHANGES.md  Include release notes

For more info: https://docs.internal.example.com/releases
"""

parser = argparse.ArgumentParser(
    description="Release manager — tag, build, and publish a new version.",
    # Preserve whitespace/formatting in description + epilog
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=EPILOG,
)

parser.add_argument("--version", required=True, metavar="X.Y.Z",
                    help="Semantic version to release (e.g. 2.3.0)")
parser.add_argument("--repo", default="all",
                    help="Target repository name (default: %(default)s)")
parser.add_argument("--notes", metavar="FILE",
                    help="Path to release-notes markdown file")
parser.add_argument("--dry-run", action="store_true",
                    help="Simulate without pushing tags or artifacts")

args = parser.parse_args()

print(f"Releasing {args.version} for repo '{args.repo}'")
if args.dry_run:
    print("DRY-RUN: no tags pushed, no artifacts built.")
else:
    print("Tagging, building, and publishing…")
if args.notes:
    print(f"Reading release notes from: {args.notes}")


if __name__ == "__main__":
    pass
