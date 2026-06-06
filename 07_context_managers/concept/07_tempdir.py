#!/usr/bin/env python3
# Context manager: tempfile.TemporaryDirectory + manual __enter__/__exit__ pattern
import os
import tempfile
from pathlib import Path


# --- Built-in: tempfile.TemporaryDirectory ---
# Automatically creates a temp dir on __enter__ and deletes it on __exit__
with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    # Write a couple files inside the temp directory
    (tmp_path / "hello.txt").write_text("Hello from temp dir!\n")
    (tmp_path / "data.csv").write_text("col1,col2\n1,a\n2,b\n")

    print(f"Temp dir: {tmp}")
    print(f"Contents: {sorted(p.name for p in tmp_path.iterdir())}")

# After the with-block, the directory and its contents are gone
assert not Path(tmp).exists(), "TemporaryDirectory should clean up after itself"
print(f"Dir exists after exit? {Path(tmp).exists()}")


# --- Manual pattern: implementing __enter__/__exit__ from scratch ---
# This mirrors what TemporaryDirectory does internally
class ManagedTempDir:
    """Create a temp directory, yield its path, and clean up on exit."""

    def __init__(self, prefix="mytemp_", suffix=""):
        self.prefix = prefix
        self.suffix = suffix

    def __enter__(self):
        # Create the unique temporary directory
        self.path = Path(tempfile.mkdtemp(prefix=self.prefix, suffix=self.suffix))
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Recursively remove everything inside, then the dir itself
        import shutil
        if self.path.exists():
            shutil.rmtree(self.path)
        return False  # propagate exceptions normally


# --- Context manager that only creates a temp dir if needed ---
class OptionalTempDir:
    """Use a permanent directory if given, otherwise create a temporary one."""

    def __init__(self, directory=None):
        self.given_dir = directory
        self._cleanup = False

    def __enter__(self):
        if self.given_dir:
            path = Path(self.given_dir)
            path.mkdir(parents=True, exist_ok=True)
        else:
            path = Path(tempfile.mkdtemp(prefix="optional_"))
            self._cleanup = True
        self.path = path
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._cleanup and self.path.exists():
            import shutil
            shutil.rmtree(self.path)
        return False


if __name__ == "__main__":
    # Use our manual implementation
    with ManagedTempDir(prefix="demo_") as d:
        (d / "scratch.txt").write_text("Temporary workspace\n")
        print(f"Manual temp dir: {d}")
        print(f"  scratch.txt exists: {(d / 'scratch.txt').exists()}")

    print(f"  After exit, dir exists: {d.exists()}")

    # Optional: reuse an existing dir
    with OptionalTempDir("/tmp/persistent_workspace") as d:
        (d / "notes.md").write_text("# Persistent notes\n")
        print(f"Persistent dir: {d}")
    print(f"  Still exists: {d.exists()}")  # True — not cleaned up
