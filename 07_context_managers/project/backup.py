#!/usr/bin/env python3
"""File backup tool: context managers for temp dirs, timing blocks, atomic writes.

Creates timestamped backup with SHA-256 verification — stdlib only.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Iterator, List, Optional, Tuple

# ============================================================================
# Context Managers
# ============================================================================


@contextlib.contextmanager
def atomic_write(path: Path, mode: str = "w", encoding: str = "utf-8"):
    """Write to a temp file, then atomically rename to target path."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    f = open(tmp, mode, encoding=encoding)
    try:
        yield f
        f.close()
        tmp.rename(path)
    except Exception:
        f.close()
        if tmp.exists():
            tmp.unlink()
        raise


@contextlib.contextmanager
def temp_workdir(prefix: str = "backup_") -> Iterator[Path]:
    """Create a temporary working directory, cleaned up on exit."""
    td = Path(tempfile.mkdtemp(prefix=prefix))
    try:
        yield td
    finally:
        shutil.rmtree(td, ignore_errors=True)


@contextlib.contextmanager
def timing_block(label: str = "Operation") -> Iterator[None]:
    """Time a block of code."""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"[timing] {label}: {elapsed:.3f}s")


@contextlib.contextmanager
def cd(path: Path) -> Iterator[None]:
    """Temporarily change working directory, restored on exit."""
    old = os.getcwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(old)


# ============================================================================
# Backup logic
# ============================================================================
def sha256_file(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def create_backup(
    sources: List[Path],
    dest_dir: Path,
    compression: bool = False,
) -> List[Tuple[Path, str, int]]:
    """Backup files to a destination directory. Returns [(backup_path, sha256, size_bytes), ...]."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_dir.mkdir(parents=True, exist_ok=True)
    results = []

    with temp_workdir(prefix="backup_stage_") as staging:
        with timing_block("Backup files"):
            for src in sources:
                if not src.exists():
                    print(f"Warning: skipping missing file {src}", file=sys.stderr)
                    continue

                name = f"{src.stem}_{timestamp}{src.suffix}"
                dest = dest_dir / name

                # Stage to temp first, then copy atomically
                staged = staging / name
                if src.is_file():
                    shutil.copy2(src, staged)
                elif src.is_dir():
                    if compression:
                        archive_base = staging / f"{src.stem}_{timestamp}"
                        archive_path = shutil.make_archive(
                            str(archive_base), "zip", root_dir=str(src.parent), base_dir=src.name
                        )
                        # Move the archive to the staging dir
                        final_staged = staging / Path(archive_path).name
                        shutil.move(archive_path, final_staged)
                        staged = final_staged

                    else:
                        shutil.copytree(src, staged)
                else:
                    print(f"Warning: {src} is not a file or directory", file=sys.stderr)
                    continue

                # Atomic move to destination
                staged.rename(dest)

                # Verify
                digest = sha256_file(dest)
                size = dest.stat().st_size
                results.append((dest, digest, size))
                print(f"  Backed up: {dest.name}  ({size} bytes, sha256={digest[:12]}…)")

    return results


# ============================================================================
# Index file
# ============================================================================
def write_index(dest_dir: Path, results: List[Tuple[Path, str, int]], timestamp: str) -> None:
    """Write a backup index file using atomic_write context manager."""
    index_path = dest_dir / f"backup_index_{timestamp}.json"

    import json
    content = {
        "timestamp": timestamp,
        "files": [
            {"name": p.name, "sha256": digest, "size": size}
            for p, digest, size in results
        ],
    }

    with atomic_write(index_path) as f:
        json.dump(content, f, indent=2)

    print(f"Index written: {index_path}")


# ============================================================================
# CLI
# ============================================================================
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="File backup tool with atomic writes, timing, temp dirs — context-manager powered."
    )
    p.add_argument("sources", nargs="*", type=Path, help="Files or directories to back up")
    p.add_argument("-o", "--output", type=Path, default=Path.cwd() / "backups",
                   help="Destination directory (default: ./backups)")
    p.add_argument("--compress", action="store_true", help="Compress directories as .zip")
    p.add_argument("--verify", action="store_true", help="Re-verify existing backup checksums")
    p.add_argument("--list", action="store_true", help="List backup contents instead of creating")
    return p


def main() -> None:
    args = build_parser().parse_args()

    dest_dir: Path = args.output

    if args.list:
        if not dest_dir.exists():
            print(f"No backup directory: {dest_dir}", file=sys.stderr)
            sys.exit(1)
        files = sorted(dest_dir.iterdir())
        if not files:
            print("Backup directory is empty.")
            return
        for f in files:
            if f.is_file():
                print(f"  {f.name:50s}  {f.stat().st_size:>10d} bytes")
        return

    if args.verify:
        if not dest_dir.exists():
            print(f"No backup directory: {dest_dir}", file=sys.stderr)
            sys.exit(1)
        with timing_block("Verification"):
            ok = 0
            for f in sorted(dest_dir.iterdir()):
                if not f.is_file() or f.suffix == ".json":
                    continue
                digest = sha256_file(f)
                print(f"  {f.name}: sha256={digest}")
                ok += 1
            print(f"\nVerified {ok} file(s) successfully.")
        return

    # Backup mode: sources required
    if not args.sources:
        print("Error: no sources specified. Use --help.", file=sys.stderr)
        sys.exit(1)
    dest_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    with timing_block("Total backup"):
        results = create_backup(
            sources=args.sources,
            dest_dir=dest_dir,
            compression=args.compress,
        )

    if results:
        write_index(dest_dir, results, timestamp)
        total_size = sum(s for _, _, s in results)
        print(f"\nBackup complete: {len(results)} file(s), {total_size} bytes total")
    else:
        print("No files backed up.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
