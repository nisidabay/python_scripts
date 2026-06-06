#!/usr/bin/env python3
"""Filesystem exercises: directory walking, duplicate detection, atomic writes, watchers."""

import hashlib
import os
import shutil
import tarfile
import tempfile
import time
from pathlib import Path

# Shared test directory — created once, cleaned up at end
TEST_DIR = Path(tempfile.mkdtemp(prefix="fs_exercises_"))


def setup_test_tree(base: Path) -> None:
    """Create a small directory tree with known files for exercises."""
    (base / "docs").mkdir(parents=True, exist_ok=True)
    (base / "images").mkdir(parents=True, exist_ok=True)
    (base / "images" / "thumbs").mkdir(parents=True, exist_ok=True)

    (base / "docs" / "readme.txt").write_text("Hello world")
    (base / "docs" / "notes.md").write_text("# Notes\nProject notes here.")
    (base / "images" / "logo.png").write_bytes(b"\x89PNG fake data")
    (base / "images" / "banner.png").write_bytes(b"\x89PNG fake banner data")
    (base / "images" / "thumbs" / "logo_thumb.png").write_bytes(b"\x89PNG fake data")  # duplicate of logo.png
    (base / "data.csv").write_text("name,age\nAlice,30\nBob,25\n")


# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 1: Walk directory tree — report total size per extension
# ═══════════════════════════════════════════════════════════════════════════════

def walk_and_report_extension_sizes(root: Path) -> dict[str, int]:
    """Walk the entire tree and sum file sizes grouped by extension."""
    ext_sizes: dict[str, int] = {}
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            fpath = Path(dirpath) / fname
            ext = fpath.suffix.lower() or "(no ext)"  # handle files with no extension
            size = fpath.stat().st_size
            ext_sizes[ext] = ext_sizes.get(ext, 0) + size
    return ext_sizes

# Run
setup_test_tree(TEST_DIR)
result1 = walk_and_report_extension_sizes(TEST_DIR)
print("Exercise 1 — Extension sizes:")
for ext, size in sorted(result1.items()):
    print(f"  {ext:>10}: {size:>6} bytes")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 2: Find duplicate files by hash (SHA-256)
# ═══════════════════════════════════════════════════════════════════════════════

def find_duplicates(root: Path) -> dict[str, list[Path]]:
    """Return groups of files with identical SHA-256 hashes."""
    hash_map: dict[str, list[Path]] = {}
    for fpath in root.rglob("*"):
        if fpath.is_file():
            digest = hashlib.sha256(fpath.read_bytes()).hexdigest()
            hash_map.setdefault(digest, []).append(fpath)
    # Keep only groups with more than one file
    return {h: paths for h, paths in hash_map.items() if len(paths) > 1}

dupes = find_duplicates(TEST_DIR)
print(f"Exercise 2 — Duplicate groups found: {len(dupes)}")
for digest, files in dupes.items():
    print(f"  hash={digest[:12]}... → {len(files)} files: {[f.name for f in files]}")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 3: Atomic file replace (write to temp, then rename)
# ═══════════════════════════════════════════════════════════════════════════════

def atomic_write(path: Path, content: str) -> None:
    """Write content to path atomically — partial writes are never seen."""
    # Write to a temp file in the same directory (same filesystem → rename is atomic)
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        tmp.write_text(content, encoding="utf-8")
        tmp.replace(path)  # os.replace is atomic on POSIX, best-effort on Windows
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)

target = TEST_DIR / "atomic_demo.txt"
atomic_write(target, "Version 1 — initial content")
assert target.read_text() == "Version 1 — initial content"
atomic_write(target, "Version 2 — updated atomically")
assert target.read_text() == "Version 2 — updated atomically"
print("Exercise 3 — Atomic write: both versions written without corruption")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 4: Watch a directory for changes (polling with mtime)
# ═══════════════════════════════════════════════════════════════════════════════

def watch_directory(path: Path, interval: float = 0.2, max_cycles: int = 3):
    """Poll a directory and yield (event, path) tuples when files change.

    In production you'd use inotify / watchdog, but polling mtime is portable
    and illustrates the concept clearly.
    """
    # Snapshot initial mtimes
    snapshot: dict[Path, float] = {}
    for f in path.rglob("*"):
        if f.is_file():
            snapshot[f] = f.stat().st_mtime

    for _ in range(max_cycles):
        time.sleep(interval)
        current: dict[Path, float] = {}
        for f in path.rglob("*"):
            if f.is_file():
                current[f] = f.stat().st_mtime

        # Detect new/modified files
        for fpath, mtime in current.items():
            if fpath not in snapshot:
                yield ("created", fpath)
            elif mtime > snapshot[fpath]:
                yield ("modified", fpath)

        # Detect deleted files
        for fpath in snapshot:
            if fpath not in current:
                yield ("deleted", fpath)

        snapshot = current

# Demonstrate: touch a new file while "watching"
import threading

def delayed_touch():
    time.sleep(0.3)
    (TEST_DIR / "watched_new.txt").write_text("I appeared after start!")

watcher_thread = threading.Thread(target=delayed_touch, daemon=True)
watcher_thread.start()

print("Exercise 4 — Directory watcher events:")
for event, fpath in watch_directory(TEST_DIR, interval=0.2, max_cycles=3):
    print(f"  [{event.upper():>8}] {fpath.relative_to(TEST_DIR)}")
watcher_thread.join()
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# BONUS: Archive files older than N days into a tar.gz
# ═══════════════════════════════════════════════════════════════════════════════

def archive_old_files(source: Path, archive_path: Path, days: float = 0):
    """Create a tar.gz of files in source older than `days`. Days=0 includes all."""
    cutoff = time.time() - (days * 86400)
    with tarfile.open(archive_path, "w:gz") as tar:
        for fpath in source.rglob("*"):
            if fpath.is_file() and fpath.stat().st_mtime < cutoff:
                # arcname relative to source so the archive isn't full of absolute paths
                tar.add(fpath, arcname=fpath.relative_to(source))
    return archive_path.stat().st_size

# Archive everything (days=0 → all files are "older than 0 days")
bonus_archive = TEST_DIR / "backup.tar.gz"
archive_size = archive_old_files(TEST_DIR, bonus_archive, days=0)
print(f"BONUS — Archive created: {bonus_archive.name} ({archive_size} bytes)")
# Verify
assert bonus_archive.exists() and archive_size > 0
print("---")

# Cleanup
shutil.rmtree(TEST_DIR, ignore_errors=True)
print("All filesystem exercises passed.")
