#!/usr/bin/env python3
# exercises.py — Group 07: Context Managers
# 4 solved exercises + BONUS. Run: python3 exercises.py

import contextlib
import io
import os
import shutil
import tempfile
import time
from pathlib import Path
from contextlib import contextmanager, ExitStack, redirect_stdout


# ============================================================
# Exercise 1: Class-based context manager for timing blocks
# ============================================================

class Timer:
    """Context manager: measure elapsed wall-clock time inside a with-block.

    __enter__ is called at the start. __exit__ is called at the end,
    even if an exception occurs. Returning False means exceptions propagate.
    """

    def __init__(self, label: str = "Block"):
        self.label = label

    def __enter__(self):
        self.start = time.perf_counter()   # high-resolution monotonic clock
        return self                         # caller gets the Timer instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"  [{self.label}] took {self.elapsed:.6f} seconds")
        return False  # don't suppress any exceptions

print("Exercise 1:")
with Timer("Heavy computation") as t:
    total = sum(i * i for i in range(5_000_000))
print(f"  Sum of squares: {total}")

# Verify the elapsed attribute is accessible after the block
assert hasattr(t, "elapsed") and t.elapsed > 0

# Nested timers — exit order is LIFO (inner exits first)
with Timer("outer") as t_outer:
    with Timer("inner") as t_inner:
        time.sleep(0.01)
print(f"  outer: {t_outer.elapsed:.4f}s, inner: {t_inner.elapsed:.4f}s")
assert t_outer.elapsed >= t_inner.elapsed
print("---")


# ============================================================
# Exercise 2: @contextmanager generator for temporary directory
# ============================================================

@contextmanager
def temporary_workspace(prefix: str = "workspace_"):
    """Generator-based context manager: create a temp dir, yield it, clean up.

    Everything before `yield` runs on __enter__.
    Everything after `yield` runs on __exit__ (including finally).
    """
    tmp_path = Path(tempfile.mkdtemp(prefix=prefix))
    try:
        yield tmp_path  # hand control to the with-block
    finally:
        # Always clean up, even if the with-block raises
        if tmp_path.exists():
            shutil.rmtree(tmp_path)

print("Exercise 2:")
with temporary_workspace(prefix="carlos_") as ws:
    print(f"  Workspace created at: {ws}")
    # Write some files inside the temporary workspace
    (ws / "notas.txt").write_text("Notas de Carlos: repasar pathlib\n")
    (ws / "datos.csv").write_text("nombre,edad\nCarlos,34\nAna,28\n")
    contents = sorted(p.name for p in ws.iterdir())
    print(f"  Contents: {contents}")
    assert "notas.txt" in contents
    assert "datos.csv" in contents

# After the with-block, the directory is gone
print(f"  Workspace still exists? {ws.exists()}")
assert not ws.exists(), "temporary_workspace should clean up after itself"
print("---")


# ============================================================
# Exercise 3: contextlib.ExitStack to manage multiple resources
# ============================================================

def count_lines(filepath: Path) -> int:
    """Count lines using a regular open."""
    return sum(1 for _ in filepath.open())

print("Exercise 3:")

# Simulate managing multiple resources that may enter/exit dynamically
with ExitStack() as stack:
    # Create temp files for Carlos's project
    files = [
        stack.enter_context(tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                                         delete=False))
        for _ in range(3)
    ]
    # NamedTemporaryFile is a context manager; ExitStack ensures all are cleaned up

    # Write data into each file
    data_files = [
        "Línea 1\nLínea 2\nLínea 3\n",           # 3 lines
        "Solo una línea\n",                        # 1 line
        "Primera\nSegunda\nTercera\nCuarta\n",     # 4 lines
    ]
    for f, content in zip(files, data_files):
        f.write(content)
        f.flush()

    file_paths = [Path(f.name) for f in files]
    # Count lines while files are open
    line_counts = [count_lines(p) for p in file_paths]
    print(f"  Files: {[p.name for p in file_paths]}")
    print(f"  Line counts: {line_counts}")
    assert line_counts == [3, 1, 4]

    # Manually clean up the temp files since we used delete=False
    for p in file_paths:
        p.unlink(missing_ok=True)

print("---")


# ============================================================
# Exercise 4: Nested context managers
#            (open two files, read both)
# ============================================================

print("Exercise 4:")
# Create two temp files to read
tmp_dir = Path(tempfile.mkdtemp(prefix="ex04_"))
file_a = tmp_dir / "autores.txt"
file_b = tmp_dir / "libros.txt"

file_a.write_text("Carlos\nAna\nLuis\n")
file_b.write_text("El Quijote\nCien años de soledad\nRayuela\n")

# Nested context managers: open both files in one `with` statement
# Both are guaranteed to close when the block ends (even on exception)
with open(file_a, "r", encoding="utf-8") as fa, \
     open(file_b, "r", encoding="utf-8") as fb:
    autores = [line.strip() for line in fa]
    libros = [line.strip() for line in fb]

# Zip them together into author → book pairs
pairs = list(zip(autores, libros))
for autor, libro in pairs:
    print(f"  {autor} escribió '{libro}'")

assert pairs == [
    ("Carlos", "El Quijote"),
    ("Ana", "Cien años de soledad"),
    ("Luis", "Rayuela"),
]

# Cleanup
file_a.unlink()
file_b.unlink()
tmp_dir.rmdir()
print("---")


# ============================================================
# BONUS: redirect_stdout context manager that captures print
#        output
# ============================================================

print("BONUS:   redirect_stdout — capture print() output")

# redirect_stdout: temporarily replace sys.stdout with an io.StringIO
buffer = io.StringIO()

def generate_report(name: str, score: int) -> None:
    """Function that prints — output can be captured via redirect_stdout."""
    print(f"INFORME DE RENDIMIENTO")
    print(f"======================")
    print(f"Nombre:  {name}")
    print(f"Puntaje: {score}/100")
    if score >= 90:
        print(f"Estado:  EXCELENTE")
    elif score >= 70:
        print(f"Estado:  APROBADO")
    else:
        print(f"Estado:  REPROBADO")

# Capture the output
with redirect_stdout(buffer):
    generate_report("Carlos", 94)

captured = buffer.getvalue()
print("  Captured output:")
for line in captured.strip().splitlines():
    print(f"    | {line}")

assert "Carlos" in captured
assert "94/100" in captured
assert "EXCELENTE" in captured

# Verify stdout is restored after the block
print("  stdout restored — this prints normally")
import sys
assert sys.stdout is not buffer, "Stdout should be restored"

# Also capture another report
buffer2 = io.StringIO()
with redirect_stdout(buffer2):
    generate_report("Ana", 82)

assert "Ana" in buffer2.getvalue()
assert "APROBADO" in buffer2.getvalue()

print("---")
print("✅ All Group 07 exercises passed!")
