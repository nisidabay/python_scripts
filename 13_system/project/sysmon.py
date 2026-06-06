#!/usr/bin/env python3
"""System monitor CLI — CPU%, memory, disk, running processes, battery."""

import argparse
import os
import re
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ── helpers ──────────────────────────────────────────────────────────


def get_cpu_usage() -> dict:
    """Parse /proc/stat for CPU usage percentage."""
    try:
        with open("/proc/stat") as fh:
            line = fh.readline()
        parts = line.split()
        if parts[0] != "cpu":
            return {"error": "unexpected /proc/stat format"}

        # user nice system idle iowait irq softirq steal guest guest_nice
        values = list(map(int, parts[1:]))
        idle = values[3] + (values[4] if len(values) > 4 else 0)  # idle + iowait
        total = sum(values)
        return {"used_percent": round((1 - idle / total) * 100, 1), "total_ticks": total}
    except Exception as exc:
        return {"error": str(exc)}


def get_memory() -> dict:
    """Parse /proc/meminfo for memory stats."""
    try:
        mem = {}
        with open("/proc/meminfo") as fh:
            for line in fh:
                if ":" in line:
                    key, val = line.split(":", 1)
                    val = int(val.strip().split()[0])  # kB
                    mem[key.strip()] = val

        total = mem.get("MemTotal", 0)
        available = mem.get("MemAvailable", 0)
        used = total - available
        percent = round((used / total) * 100, 1) if total > 0 else 0
        return {
            "total_kb": total,
            "used_kb": used,
            "available_kb": available,
            "used_percent": percent,
            "swap_total_kb": mem.get("SwapTotal", 0),
            "swap_free_kb": mem.get("SwapFree", 0),
        }
    except Exception as exc:
        return {"error": str(exc)}


def get_disk_usage(path: str = "/") -> dict:
    """Get disk usage via os.statvfs."""
    try:
        st = os.statvfs(path)
        total = st.f_blocks * st.f_frsize
        free = st.f_bfree * st.f_frsize
        used = total - free
        percent = round((used / total) * 100, 1) if total > 0 else 0
        return {
            "path": path,
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
            "used_percent": percent,
        }
    except Exception as exc:
        return {"error": str(exc), "path": path}


def get_processes(top_n: int = 20, sort_by: str = "cpu") -> list[dict]:
    """Get top processes by CPU or memory using ps."""
    try:
        if sort_by == "cpu":
            sort_flag = "--sort=-%cpu"
        else:
            sort_flag = "--sort=-%mem"

        result = subprocess.run(
            ["ps", "aux", sort_flag, "--no-headers"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode != 0:
            return [{"error": result.stderr.strip()}]

        procs = []
        for line in result.stdout.strip().splitlines()[:top_n]:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                procs.append({
                    "user": parts[0],
                    "pid": int(parts[1]),
                    "cpu": float(parts[2]),
                    "mem": float(parts[3]),
                    "vsz": int(parts[4]),
                    "rss": int(parts[5]),
                    "command": parts[10][:80],
                })
        return procs
    except Exception as exc:
        return [{"error": str(exc)}]


def get_battery() -> dict:
    """Read battery status from /sys/class/power_supply."""
    try:
        base = Path("/sys/class/power_supply")
        if not base.exists():
            return {"status": "no battery"}

        for bat_dir in sorted(base.iterdir()):
            if bat_dir.name.startswith("BAT") or bat_dir.name.startswith("battery"):
                capacity = (bat_dir / "capacity").read_text().strip()
                status = (bat_dir / "status").read_text().strip()
                return {
                    "name": bat_dir.name,
                    "capacity": int(capacity),
                    "status": status,
                }

        return {"status": "no battery found"}
    except Exception as exc:
        return {"error": str(exc)}


def get_uptime() -> str:
    """Return system uptime as a human-readable string."""
    try:
        with open("/proc/uptime") as fh:
            seconds = float(fh.readline().split()[0])
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        parts = []
        if d:
            parts.append(f"{d}d")
        if h:
            parts.append(f"{h}h")
        if m:
            parts.append(f"{m}m")
        if not parts:
            parts.append(f"{s}s")
        return " ".join(parts)
    except Exception:
        return "unknown"


# ── commands ─────────────────────────────────────────────────────────


def cmd_cpu(_args) -> int:
    data = get_cpu_usage()
    if "error" in data:
        print(f"Error: {data['error']}", file=sys.stderr)
        return 1
    print(f"CPU usage: {data['used_percent']}%")
    return 0


def cmd_memory(_args) -> int:
    data = get_memory()
    if "error" in data:
        print(f"Error: {data['error']}", file=sys.stderr)
        return 1
    total_gb = data["total_kb"] / 1024**2
    used_gb = data["used_kb"] / 1024**2
    print(f"Memory: {data['used_percent']}% used ({used_gb:.1f}G / {total_gb:.1f}G)")
    print(f"Swap:   {data['swap_total_kb'] / 1024**2:.1f}G total, {data['swap_free_kb'] / 1024**2:.1f}G free")
    return 0


def cmd_disk(args) -> int:
    for path in args.paths:
        data = get_disk_usage(path)
        if "error" in data:
            print(f"{path}: Error — {data['error']}", file=sys.stderr)
        else:
            print(f"{data['path']}: {data['used_percent']}% used ({data['used_gb']}G / {data['total_gb']}G)")
    return 0


def cmd_procs(args) -> int:
    procs = get_processes(top_n=args.top, sort_by=args.sort)
    if procs and "error" in procs[0]:
        print(f"Error: {procs[0]['error']}", file=sys.stderr)
        return 1

    header = f"{'USER':<10} {'PID':>7} {'CPU%':>6} {'MEM%':>6} {'RSS(KB)':>10} COMMAND"
    print(header)
    print("-" * len(header))
    for p in procs:
        print(f"{p['user']:<10} {p['pid']:>7} {p['cpu']:>5.1f}  {p['mem']:>5.1f}  {p['rss']:>10} {p['command']}")
    return 0


def cmd_battery(_args) -> int:
    data = get_battery()
    if "error" in data:
        print(f"Error: {data['error']}", file=sys.stderr)
        return 1
    if "name" in data:
        icon = "🔋" if data.get("status") == "Charging" else "⚡"
        print(f"{icon} Battery {data['name']}: {data['capacity']}% ({data['status']})")
    else:
        print(f"Battery: {data.get('status', 'unknown')}")
    return 0


def cmd_all(_args) -> int:
    """Show a snapshot of all stats."""
    uptime = get_uptime()

    print(f"╔══════════════════════════════════════════════╗")
    print(f"║         SYSTEM MONITOR SNAPSHOT               ║")
    print(f"╠══════════════════════════════════════════════╣")
    print(f"║  Uptime: {uptime:<36}║")

    # CPU
    cpu = get_cpu_usage()
    if "error" not in cpu:
        bar = "█" * int(cpu["used_percent"] / 5) + "░" * (20 - int(cpu["used_percent"] / 5))
        print(f"║  CPU:    [{bar}] {cpu['used_percent']:>5}%{'':>10}║")

    # Memory
    mem = get_memory()
    if "error" not in mem:
        bar = "█" * int(mem["used_percent"] / 5) + "░" * (20 - int(mem["used_percent"] / 5))
        used_gb = mem["used_kb"] / 1024**2
        total_gb = mem["total_kb"] / 1024**2
        print(f"║  Memory: [{bar}] {mem['used_percent']:>5}%  {used_gb:.1f}/{total_gb:.1f}G║")

    # Disk
    disk = get_disk_usage("/")
    if "error" not in disk:
        bar = "█" * int(disk["used_percent"] / 5) + "░" * (20 - int(disk["used_percent"] / 5))
        print(f"║  Disk /: [{bar}] {disk['used_percent']:>5}%  {disk['used_gb']:.1f}/{disk['total_gb']:.1f}G║")

    # Battery
    bat = get_battery()
    if "name" in bat:
        bar = "█" * int(bat["capacity"] / 5) + "░" * (20 - int(bat["capacity"] / 5))
        icon = "🔋" if bat.get("status") == "Charging" else "⚡"
        print(f"║  Batt:   [{bar}] {bat['capacity']:>5}%  {icon} {bat['status']:<10}║")

    print(f"╚══════════════════════════════════════════════╝")
    return 0


def cmd_watch(args) -> int:
    """Continuously refresh system stats."""
    print(f"Watching system stats every {args.interval}s. Press Ctrl+C to stop.\n")

    def _handle_sigint(signum, frame):
        print("\nStopped.")
        sys.exit(0)

    signal.signal(signal.SIGINT, _handle_sigint)

    try:
        while True:
            sys.stdout.write("\033[H\033[J")  # clear screen
            cmd_all(args)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


# ── main ─────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="System monitor CLI — CPU, memory, disk, processes, battery.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("cpu", help="Show CPU usage")
    sub.add_parser("memory", help="Show memory usage")

    p_disk = sub.add_parser("disk", help="Show disk usage")
    p_disk.add_argument("paths", nargs="*", default=["/"], help="Paths to check (default: /)")

    p_procs = sub.add_parser("procs", help="Show running processes")
    p_procs.add_argument("--top", type=int, default=20, help="Show top N processes (default: 20)")
    p_procs.add_argument("--sort", choices=["cpu", "mem"], default="cpu", help="Sort by (default: cpu)")

    sub.add_parser("battery", help="Show battery status")

    sub.add_parser("all", help="Show all stats snapshot")

    p_watch = sub.add_parser("watch", help="Watch stats continuously")
    p_watch.add_argument("--interval", type=float, default=2.0, help="Refresh interval in seconds (default: 2.0)")

    args = parser.parse_args()

    commands = {
        "cpu": cmd_cpu,
        "memory": cmd_memory,
        "disk": cmd_disk,
        "procs": cmd_procs,
        "battery": cmd_battery,
        "all": cmd_all,
        "watch": cmd_watch,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
