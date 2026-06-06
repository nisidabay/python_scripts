#!/usr/bin/env python3
"""System exercises: subprocess, process listing, signal handling, encryption, daemon."""

import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 1: subprocess.run — call external command, capture output
# ═══════════════════════════════════════════════════════════════════════════════

# Run 'echo' as a subprocess and capture stdout
result = subprocess.run(
    ["echo", "Hello from subprocess!"],
    capture_output=True,
    text=True,  # return str instead of bytes
    check=True,  # raise CalledProcessError on non-zero exit
)
print("Exercise 1 — subprocess.run:")
print(f"  stdout: {result.stdout.strip()}")
print(f"  returncode: {result.returncode}")

# Demonstrate error handling
try:
    subprocess.run(["ls", "/nonexistent_dir_xyz"], capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"  Error exit code: {e.returncode}, stderr: {e.stderr.strip()}")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 2: psutil-style — list processes, CPU%, memory
# ═══════════════════════════════════════════════════════════════════════════════

def list_top_processes(limit: int = 5) -> list[dict]:
    """Return the top N processes sorted by memory usage. Uses psutil under the hood."""
    try:
        import psutil
    except ImportError:
        # Pure-Python fallback via /proc (Linux only)
        return _list_procs_proc(limit)

    procs = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
        try:
            info = proc.info
            procs.append({
                "pid": info["pid"],
                "name": info["name"] or "?",
                "cpu_pct": info["cpu_percent"] or 0.0,
                "mem_mb": (info["memory_info"].rss if info["memory_info"] else 0) / (1024 * 1024),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    procs.sort(key=lambda p: p["mem_mb"], reverse=True)
    return procs[:limit]

def _list_procs_proc(limit: int) -> list[dict]:
    """Fallback: read /proc/[pid]/status and /proc/[pid]/stat for basic info."""
    procs = []
    for entry in os.scandir("/proc"):
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        try:
            status_path = Path(f"/proc/{pid}/status")
            stat_path = Path(f"/proc/{pid}/stat")
            if not status_path.exists():
                continue

            name = "?"
            vm_rss = 0
            for line in status_path.read_text().splitlines():
                if line.startswith("Name:"):
                    name = line.split(":", 1)[1].strip()
                elif line.startswith("VmRSS:"):
                    vm_rss = int(line.split()[1])  # kB

            procs.append({
                "pid": pid,
                "name": name,
                "cpu_pct": 0.0,  # would need two snapshots for CPU%
                "mem_mb": vm_rss / 1024,
            })
        except (OSError, PermissionError):
            continue

    procs.sort(key=lambda p: p["mem_mb"], reverse=True)
    return procs[:limit]

top = list_top_processes(limit=5)
print(f"Exercise 2 — Top {len(top)} processes by memory:")
for p in top:
    print(f"  PID {p['pid']:>6} | {p['name']:<20} | mem={p['mem_mb']:7.1f} MB")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 3: Signal handler for graceful shutdown
# ═══════════════════════════════════════════════════════════════════════════════

shutdown_flag: bool = False

def handle_signal(signum: int, frame):
    """Catch SIGTERM/SIGINT and set a flag for graceful shutdown."""
    global shutdown_flag
    sig_name = signal.Signals(signum).name
    print(f"\n  Received {sig_name} — initiating graceful shutdown...")
    shutdown_flag = True

# Register handlers
signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)

print("Exercise 3 — Signal handler registered:")
sigterm_handler = signal.getsignal(signal.SIGTERM)
sigint_handler = signal.getsignal(signal.SIGINT)
print(f"  SIGTERM handler: {getattr(sigterm_handler, '__name__', sigterm_handler)}")
print(f"  SIGINT  handler: {getattr(sigint_handler, '__name__', sigint_handler)}")
print("  (Handlers set — not triggering in test to avoid killing the script)")
print("  Pattern: while not shutdown_flag: do_work(); cleanup()")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 4: Encrypt/decrypt a file with Fernet (symmetric encryption)
# ═══════════════════════════════════════════════════════════════════════════════

from cryptography.fernet import Fernet

tmpdir = Path(tempfile.mkdtemp(prefix="crypto_exercise_"))

# 1. Generate a key (keep this secret!)
key = Fernet.generate_key()
cipher = Fernet(key)

# 2. Write a plaintext file
plaintext = "TOP SECRET: The launch code is 4-8-15-16-23-42."
original_file = tmpdir / "secret.txt"
original_file.write_text(plaintext)

# 3. Encrypt: read bytes, encrypt, write ciphertext
encrypted_file = tmpdir / "secret.encrypted"
encrypted_file.write_bytes(cipher.encrypt(original_file.read_bytes()))

# 4. Decrypt: read ciphertext, decrypt, verify
decrypted = cipher.decrypt(encrypted_file.read_bytes()).decode()
decrypted_file = tmpdir / "secret.decrypted"
decrypted_file.write_text(decrypted)

print("Exercise 4 — Fernet encrypt/decrypt:")
print(f"  Key (first 20 chars): {key.decode()[:20]}...")
print(f"  Original  ({original_file.stat().st_size} B): {plaintext}")
print(f"  Encrypted ({encrypted_file.stat().st_size} B): {encrypted_file.read_bytes()[:40]}...")
print(f"  Decrypted ({decrypted_file.stat().st_size} B): {decrypted_file.read_text()}")
assert plaintext == decrypted, "Round-trip failed!"
print(f"  Round-trip verified: plaintext == decrypted")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# BONUS: Daemonize — double-fork pattern to background a process
# ═══════════════════════════════════════════════════════════════════════════════

def daemonize(
    pidfile: Path | None = None,
    workdir: str = "/",
    stdin: str = "/dev/null",
    stdout: str = "/dev/null",
    stderr: str = "/dev/null",
) -> None:
    """Double-fork sequence to detach from the controlling terminal.

    This is the classic Unix daemon pattern:
    1. Fork → parent exits, child continues
    2. setsid() → become session leader, detach from terminal
    3. Fork again → grandchild can never re-acquire a terminal
    4. Redirect stdio to /dev/null, set umask, chdir to /

    NOTE: Not actually called — this is demonstration code only.
    """
    # First fork
    pid = os.fork()
    if pid > 0:
        os._exit(0)  # parent exits

    # Child becomes session leader (detaches from terminal)
    os.setsid()

    # Second fork — grandchild can never re-acquire controlling terminal
    pid = os.fork()
    if pid > 0:
        os._exit(0)

    # Grandchild is now fully daemonized
    os.umask(0o022)
    os.chdir(workdir)

    # Redirect standard file descriptors to /dev/null
    for fd in range(3):
        try:
            os.close(fd)
        except OSError:
            pass
    os.open(stdin, os.O_RDONLY)
    os.open(stdout, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    os.open(stderr, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)

    # Write PID file if requested
    if pidfile:
        pidfile.write_text(str(os.getpid()))

    # Daemon loop would go here...
    # while True: do_work()

print("BONUS — Daemon pattern: double-fork explained")
print("  See daemonize() function above for the full implementation.")
print("  1. fork() → parent exits")
print("  2. os.setsid() → detach from terminal")
print("  3. fork() again → can never re-acquire terminal")
print("  4. Redirect stdio, set umask, chdir('/')")
print("---")

# Cleanup
import shutil
shutil.rmtree(tmpdir, ignore_errors=True)
print("All system exercises passed.")
