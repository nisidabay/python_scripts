#!/usr/bin/env python3
# Modern file paths: Path objects replace os.path string juggling.

from pathlib import Path
import tempfile

# Home directory — cross-platform, no os.path.expanduser()
home = Path.home()
docs = home / "Documents"  # / operator joins paths, no os.path.join()

# Create a temp file to demonstrate read/write
tmp = Path(tempfile.mkdtemp())
report = tmp / "report.txt"
report.write_text("Carlos: 92\nAna: 88\nLuis: 95\n")  # one-liner, auto-close

# Read back — Path handles encoding, closing
content = report.read_text()  # no open()/close() ceremony
print(f"Read {len(content)} bytes from {report}")

# iterdir: list directory contents without os.listdir
tmp.mkdir(exist_ok=True)  # idempotent directory creation
for child in tmp.iterdir():  # yields Path objects, not strings
    print(f"  {child.name} ({'dir' if child.is_dir() else 'file'})")

# glob: pattern matching, recursive with **
logs = tmp / "logs"
logs.mkdir()
(logs / "app_2024.log").touch()
(logs / "app_2025.log").touch()
matches = list(tmp.glob("**/*.log"))  # recursive glob since Python 3.5
print(f"Found {len(matches)} log files via glob")

# Path parts: inspect without splitting strings
print(f"stem={report.stem}, suffix={report.suffix}, parent={report.parent}")

# Cleanup — bottom-up: deepest first so dirs are empty when rmdir'd
for f in sorted(tmp.rglob("*"), key=lambda p: len(p.parts), reverse=True):
    f.unlink() if f.is_file() else f.rmdir()
tmp.rmdir()

if __name__ == "__main__":
    assert isinstance(home, Path), "home() should return a Path"
    print("pathlib checks passed")
