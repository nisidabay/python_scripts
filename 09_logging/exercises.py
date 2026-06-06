#!/usr/bin/env python3
"""Logging exercises: handlers, hierarchy, rotation, filters, JSON output."""

import io
import json
import logging
import logging.handlers
import os
import tempfile
from pathlib import Path

LOG_DIR = Path(tempfile.mkdtemp(prefix="logging_exercises_"))

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 1: Basic logger with file handler and formatter
# ═══════════════════════════════════════════════════════════════════════════════

logger1 = logging.getLogger("ex1_basic")
logger1.setLevel(logging.DEBUG)  # capture everything for the exercise
# Avoid duplicate handlers if run multiple times
logger1.handlers.clear()

fh = logging.FileHandler(LOG_DIR / "ex1_basic.log")
fh.setLevel(logging.DEBUG)
fmt = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
fh.setFormatter(fmt)
logger1.addHandler(fh)

logger1.debug("Debug message — fine-grained diagnostic")
logger1.info("Server started on port 8080")
logger1.warning("Disk usage at 85%")
logger1.error("Connection timeout after 30s")

# Read back and show
print("Exercise 1 — File handler output:")
print(Path(LOG_DIR / "ex1_basic.log").read_text())
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 2: Logger hierarchy (parent → child, propagation)
# ═══════════════════════════════════════════════════════════════════════════════

parent = logging.getLogger("myapp")
parent.setLevel(logging.DEBUG)
parent.handlers.clear()

# Parent writes to a string buffer so we can inspect output
parent_buf = io.StringIO()
ph = logging.StreamHandler(parent_buf)
ph.setFormatter(logging.Formatter("%(name)-12s | %(levelname)-8s | %(message)s"))
parent.addHandler(ph)

# Child inherits level and handlers from parent via propagation
child = logging.getLogger("myapp.database")
# Child does NOT add its own handler — relies on propagation to parent

parent.info("Parent: app initialized")
child.warning("Child: DB pool exhausted")   # propagates up to parent handler

# Demonstrate turning OFF propagation
child.propagate = False
isolated_buf = io.StringIO()
child.addHandler(logging.StreamHandler(isolated_buf))
child.setLevel(logging.WARNING)
child.warning("Child: isolated message")     # only in child's handler
parent.info("Parent: still receiving own messages")

print("Exercise 2 — Hierarchy output:")
print(parent_buf.getvalue())
print("Isolated child output:", isolated_buf.getvalue().strip())
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 3: RotatingFileHandler (size-based rotation)
# ═══════════════════════════════════════════════════════════════════════════════

rot_log = LOG_DIR / "rotating.log"
rot_logger = logging.getLogger("ex3_rotate")
rot_logger.setLevel(logging.DEBUG)
rot_logger.handlers.clear()

# Rotate after ~200 bytes, keep 3 backups
handler = logging.handlers.RotatingFileHandler(
    rot_log, maxBytes=200, backupCount=3
)
handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%S"))

rot_logger.addHandler(handler)

# Write enough to trigger rotation
for i in range(15):
    rot_logger.info(f"Log entry {i:03d} — this line adds bytes to force rotation")

rotated_files = sorted(LOG_DIR.glob("rotating.log*"))
print(f"Exercise 3 — Rotating log produced {len(rotated_files)} files:")
for f in rotated_files:
    print(f"  {f.name}: {f.stat().st_size} bytes")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 4: Custom filter — only allow WARNING and above
# ═══════════════════════════════════════════════════════════════════════════════

class WarningAndAboveFilter(logging.Filter):
    """Filter that drops any record below WARNING level."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno >= logging.WARNING  # True = keep, False = drop

filtered_logger = logging.getLogger("ex4_filtered")
filtered_logger.setLevel(logging.DEBUG)  # logger is generous, filter restricts
filtered_logger.handlers.clear()

filter_buf = io.StringIO()
fh2 = logging.StreamHandler(filter_buf)
fh2.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
fh2.addFilter(WarningAndAboveFilter())  # attach the custom filter
filtered_logger.addHandler(fh2)

filtered_logger.debug("Debug — will be filtered out")
filtered_logger.info("Info — also filtered out")
filtered_logger.warning("Warning — passes through!")
filtered_logger.error("Error — passes through!")
filtered_logger.critical("Critical — passes through!")

print("Exercise 4 — Custom filter (WARNING+ only):")
print(filter_buf.getvalue().strip())
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# BONUS: JSON-formatted log records using a custom Formatter
# ═══════════════════════════════════════════════════════════════════════════════

class JsonFormatter(logging.Formatter):
    """Emit log records as JSON lines — ideal for structured logging pipelines."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        # Include exception info if present
        if record.exc_info and record.exc_info[1]:
            log_entry["exception"] = str(record.exc_info[1])
        return json.dumps(log_entry, ensure_ascii=False)

json_logger = logging.getLogger("ex5_json")
json_logger.setLevel(logging.DEBUG)
json_logger.handlers.clear()

json_buf = io.StringIO()
jh = logging.StreamHandler(json_buf)
jh.setFormatter(JsonFormatter())
json_logger.addHandler(jh)

json_logger.info("User logged in", extra={"user_id": 42})
try:
    1 / 0
except ZeroDivisionError:
    json_logger.exception("Division by zero caught")

print("BONUS — JSON log records:")
for line in json_buf.getvalue().strip().split("\n"):
    parsed = json.loads(line)
    print(f"  {json.dumps(parsed, indent=2)}")
print("---")

# Cleanup
import shutil
shutil.rmtree(LOG_DIR, ignore_errors=True)
print("All logging exercises passed.")
