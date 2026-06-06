#!/usr/bin/env python3
# exercises.py — Group 01: Foundations
# 4 solved exercises + BONUS. Run: python3 exercises.py

import argparse
import os
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

# ============================================================
# Exercise 1: Use pathlib to count .py files in a directory
# ============================================================

def count_py_files(directory: Path) -> int:
    """Count .py files recursively using the glob pattern."""
    return len(list(directory.rglob("*.py")))

# Create a temp directory with .py files so the exercise is self-contained
import tempfile
tmp_base = Path(tempfile.mkdtemp(prefix="ex01_"))
(tmp_base / "main.py").touch()
(tmp_base / "utils.py").touch()
(tmp_base / "data.csv").touch()         # should NOT be counted
sub = tmp_base / "subdir"
sub.mkdir()
(sub / "helpers.py").touch()

py_count = count_py_files(tmp_base)
print(f"Exercise 1: Found {py_count} .py files in {tmp_base}")
assert py_count == 3, f"Expected 3 .py files, got {py_count}"

# Cleanup
for f in sorted(tmp_base.rglob("*"), key=lambda p: -len(p.parts)):
    f.unlink() if f.is_file() else f.rmdir()
tmp_base.rmdir()
print("---")

# ============================================================
# Exercise 2: Parse command-line args with argparse
#             (--input, --verbose flags)
# ============================================================

def parse_args(argv: list[str]) -> argparse.Namespace:
    """Simulate CLI parsing — default argv=['--input','data.txt','--verbose']."""
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("--input", type=str, required=True,
                        help="Input file path")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    return parser.parse_args(argv)

# Simulate a CLI call: python3 script.py --input data.txt --verbose
simulated_argv = ["--input", "data.txt", "--verbose"]
args = parse_args(simulated_argv)
print(f"Exercise 2: input={args.input}, verbose={args.verbose}")
assert args.input == "data.txt"
assert args.verbose is True
print("---")

# ============================================================
# Exercise 3: Use a dataclass to model a Book (title, author,
#            year) + asdict for serialization
# ============================================================

@dataclass
class Book:
    title: str
    author: str
    year: int

# Create two books and convert to dict
book1 = Book(title="El ingenioso hidalgo Don Quijote de la Mancha",
             author="Miguel de Cervantes", year=1605)
book2 = Book(title="Cien años de soledad", author="Gabriel García Márquez",
             year=1967)

book_dict = asdict(book1)  # asdict converts dataclass to dict (recursive)
print(f"Exercise 3: {book1}")
print(f"           asdict → {book_dict}")
assert book_dict["title"].startswith("El ingenioso")
assert book2.year == 1967
print("---")

# ============================================================
# Exercise 4: Custom exception hierarchy + try/except/raise
# ============================================================

class AppError(Exception):
    """Base exception for the application."""
    def __init__(self, message: str, code: int = 0):
        super().__init__(message)
        self.code = code  # extra context for debugging

class ValidationError(AppError):
    """Raised when input fails business rules."""
    pass

class DatabaseError(AppError):
    """Raised when database operations fail."""
    pass

def validate_username(name: str) -> None:
    """Username must be non-empty and ≤30 chars."""
    if not name.strip():
        raise ValidationError("Username cannot be empty", code=400)
    if len(name) > 30:
        raise ValidationError(f"Username too long: {len(name)} chars", code=400)

def simulate_db_connect(host: str) -> None:
    """Simulate a database connection failure."""
    if "offline" in host:
        raise DatabaseError(f"Could not connect to {host}", code=503)

# Happy path
try:
    validate_username("Carlos")
    print(f"Exercise 4: Username 'Carlos' is valid")
except ValidationError as e:
    print(f"Unexpected error: {e}")

# Deliberate failure — catch and inspect the exception chain
try:
    simulate_db_connect("db-offline.example.com")
except DatabaseError as e:
    print(f"           Caught DatabaseError: {e} (code={e.code})")
    assert e.code == 503

# Verify exception hierarchy
assert issubclass(ValidationError, AppError)
assert issubclass(DatabaseError, AppError)
print("---")

# ============================================================
# BONUS: Build an env-var-aware config loader
#        (os.environ fallback pattern)
# ============================================================

def load_config(*, env_prefix: str = "APP_") -> dict[str, Any]:
    """Load config from environment variables with a prefix, plus defaults.

    Pattern: APP_KEY=value becomes config['key'] (lowercased).
    Falls back to hardcoded defaults when env var is missing.
    """
    defaults = {
        "host": "localhost",
        "port": 5432,
        "debug": False,
        "log_level": "INFO",
    }
    config = dict(defaults)  # start with defaults

    for key, default_val in defaults.items():
        env_key = f"{env_prefix}{key.upper()}"
        raw = os.environ.get(env_key)
        if raw is not None:
            # Cast to the same type as the default
            if isinstance(default_val, bool):
                config[key] = raw.lower() in ("1", "true", "yes")
            elif isinstance(default_val, int):
                config[key] = int(raw)
            else:
                config[key] = raw  # string
        # else: keep the default

    return config

# Simulate some env vars being set
os.environ["APP_HOST"] = "db.prod.example.com"
os.environ["APP_DEBUG"] = "1"
os.environ["APP_PORT"] = "3306"
# LOG_LEVEL is NOT set — should keep the default "INFO"

cfg = load_config()
print(f"BONUS:    host={cfg['host']}, port={cfg['port']}, "
      f"debug={cfg['debug']}, log_level={cfg['log_level']}")

assert cfg["host"] == "db.prod.example.com"
assert cfg["port"] == 3306
assert cfg["debug"] is True
assert cfg["log_level"] == "INFO"  # default preserved

# Clean up env vars we set
for key in ("APP_HOST", "APP_DEBUG", "APP_PORT"):
    del os.environ[key]

print("---")
print("✅ All Group 01 exercises passed!")
