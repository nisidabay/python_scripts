#!/usr/bin/env python3
"""Rich dashboard — live-updating system stats with progress bars, tables, panels."""

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich import box


console = Console()


# ── data collectors ──────────────────────────────────────────────────


def get_cpu_percent() -> float:
    """Read CPU usage from /proc/stat."""
    try:
        with open("/proc/stat") as fh:
            line = fh.readline()
        parts = line.split()
        values = list(map(int, parts[1:]))
        idle = values[3] + (values[4] if len(values) > 4 else 0)
        total = sum(values)
        return round((1 - idle / total) * 100, 1)
    except Exception:
        return 0.0


def get_memory_percent() -> float:
    """Read memory usage from /proc/meminfo."""
    try:
        mem = {}
        with open("/proc/meminfo") as fh:
            for line in fh:
                if ":" in line:
                    key, val = line.split(":", 1)
                    mem[key.strip()] = int(val.strip().split()[0])
        total = mem.get("MemTotal", 1)
        available = mem.get("MemAvailable", 0)
        return round(((total - available) / total) * 100, 1)
    except Exception:
        return 0.0


def get_swap_percent() -> float:
    """Read swap usage."""
    try:
        mem = {}
        with open("/proc/meminfo") as fh:
            for line in fh:
                if ":" in line:
                    key, val = line.split(":", 1)
                    mem[key.strip()] = int(val.strip().split()[0])
        total = mem.get("SwapTotal", 1)
        free = mem.get("SwapFree", 0)
        return round(((total - free) / total) * 100, 1) if total > 0 else 0.0
    except Exception:
        return 0.0


def get_disk_percent(path: str = "/") -> float:
    """Get disk usage percentage."""
    try:
        st = os.statvfs(path)
        total = st.f_blocks * st.f_frsize
        free = st.f_bfree * st.f_frsize
        return round(((total - free) / total) * 100, 1) if total > 0 else 0.0
    except Exception:
        return 0.0


def get_top_processes(n: int = 10) -> list[tuple[str, float, float]]:
    """Get top N processes by CPU, return list of (name, cpu%, mem%)."""
    try:
        result = subprocess.run(
            ["ps", "aux", "--sort=-%cpu", "--no-headers"],
            capture_output=True, text=True, timeout=3,
        )
        procs = []
        for line in result.stdout.strip().splitlines()[:n]:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                name = parts[10][:40]
                cpu = float(parts[2])
                mem = float(parts[3])
                procs.append((name, cpu, mem))
        return procs
    except Exception:
        return []


def get_uptime() -> str:
    """Get system uptime string."""
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
        parts.append(f"{s}s")
        return " ".join(parts)
    except Exception:
        return "unknown"


def get_loadavg() -> list[str]:
    """Get load averages."""
    try:
        with open("/proc/loadavg") as fh:
            return fh.readline().split()[:3]
    except Exception:
        return ["?", "?", "?"]


def get_net_stats() -> dict:
    """Get simple network byte counters from /proc/net/dev."""
    try:
        with open("/proc/net/dev") as fh:
            lines = fh.readlines()[2:]  # skip headers
        rx_total = 0
        tx_total = 0
        for line in lines:
            if ":" in line:
                _, data = line.split(":", 1)
                cols = data.split()
                if len(cols) >= 9:
                    rx_total += int(cols[0])
                    tx_total += int(cols[8])
        return {"rx_mb": round(rx_total / 1024**2, 2), "tx_mb": round(tx_total / 1024**2, 2)}
    except Exception:
        return {"rx_mb": 0, "tx_mb": 0}


def get_battery() -> str:
    """Get battery info."""
    try:
        for bat in sorted(Path("/sys/class/power_supply").iterdir()):
            if bat.name.startswith("BAT"):
                cap = (bat / "capacity").read_text().strip()
                stat = (bat / "status").read_text().strip()
                return f"{cap}% {stat}"
    except Exception:
        pass
    return "N/A"


# ── render functions ─────────────────────────────────────────────────


def make_header() -> Panel:
    """Build the header panel."""
    uptime = get_uptime()
    load1, load5, load15 = get_loadavg()
    header_text = Text()
    header_text.append("🖥  SYSMON DASHBOARD", style="bold white on blue")
    header_text.append(f"    Uptime: {uptime}    ", style="cyan")
    header_text.append(f"Load: {load1} {load5} {load15}", style="dim")
    return Panel(header_text, box=box.HEAVY)


def make_cpu_panel(cpu_pct: float) -> Panel:
    """Build CPU progress bar panel."""
    # Color based on usage
    if cpu_pct > 90:
        color = "red"
    elif cpu_pct > 70:
        color = "yellow"
    else:
        color = "green"

    bar_len = 30
    filled = int(cpu_pct / 100 * bar_len)
    bar = f"[{color}]" + "█" * filled + "[dim]░" * (bar_len - filled)

    return Panel(
        f"{bar} [bold]{cpu_pct:>5.1f}%[/bold]",
        title="CPU",
        border_style=color,
    )


def make_memory_panel(mem_pct: float, swap_pct: float) -> Panel:
    """Build memory usage panel."""
    if mem_pct > 90:
        color = "red"
    elif mem_pct > 70:
        color = "yellow"
    else:
        color = "green"

    bar_len = 30
    filled = int(mem_pct / 100 * bar_len)
    mem_bar = f"[{color}]" + "█" * filled + "[dim]░" * (bar_len - filled)

    filled_s = int(swap_pct / 100 * bar_len) if swap_pct > 0 else 0
    swap_bar = f"[yellow]" + "█" * filled_s + "[dim]░" * (bar_len - filled_s)

    content = f"{mem_bar} [bold]{mem_pct:>5.1f}%[/bold]\n"
    content += f"SWAP  {swap_bar} [bold]{swap_pct:>5.1f}%[/bold]"

    return Panel(content, title="Memory", border_style=color)


def make_disk_panel(disk_pct: float) -> Panel:
    """Build disk usage panel."""
    if disk_pct > 90:
        color = "red"
    elif disk_pct > 75:
        color = "yellow"
    else:
        color = "green"

    bar_len = 30
    filled = int(disk_pct / 100 * bar_len)
    bar = f"[{color}]" + "█" * filled + "[dim]░" * (bar_len - filled)

    return Panel(
        f"{bar} [bold]{disk_pct:>5.1f}%[/bold] used on /",
        title="Disk",
        border_style=color,
    )


def make_process_table(procs: list[tuple[str, float, float]]) -> Table:
    """Build top processes table."""
    table = Table(title="Top Processes (by CPU)", box=box.ROUNDED, expand=True)
    table.add_column("Process", style="cyan", no_wrap=True)
    table.add_column("CPU %", justify="right", style="green")
    table.add_column("MEM %", justify="right", style="yellow")

    for name, cpu, mem in procs[:10]:
        table.add_row(name, f"{cpu:.1f}", f"{mem:.1f}")

    return table


def make_info_panel() -> Panel:
    """Build extra info panel: network, battery."""
    net = get_net_stats()
    bat = get_battery()

    lines = []
    lines.append(f"Network   RX: {net['rx_mb']:.1f} MB   TX: {net['tx_mb']:.1f} MB")
    lines.append(f"Battery   {bat}")

    return Panel("\n".join(lines), title="Info", border_style="blue")


# ── main loop ────────────────────────────────────────────────────────


def build_dashboard(cpu_pct: float, mem_pct: float, swap_pct: float, disk_pct: float,
                    procs: list[tuple[str, float, float]]) -> Layout:
    """Compose the full dashboard layout."""
    layout = Layout()

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body"),
    )

    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right", ratio=2),
    )

    layout["left"].split(
        Layout(make_cpu_panel(cpu_pct)),
        Layout(make_memory_panel(mem_pct, swap_pct)),
        Layout(make_disk_panel(disk_pct)),
        Layout(make_info_panel()),
    )

    layout["right"].update(make_process_table(procs))

    layout["header"].update(make_header())

    return layout


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rich dashboard — live-updating system stats with progress bars, tables, panels.",
    )
    parser.add_argument(
        "--interval", "-n", type=float, default=1.0,
        help="Refresh interval in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Print one snapshot and exit (no live refresh)",
    )
    args = parser.parse_args()

    if args.once:
        cpu = get_cpu_percent()
        mem = get_memory_percent()
        swap = get_swap_percent()
        disk = get_disk_percent()
        procs = get_top_processes()
        layout = build_dashboard(cpu, mem, swap, disk, procs)
        console.print(layout)
        return 0

    # Live updating mode
    console.clear()
    with Live(console=console, screen=True, refresh_per_second=4) as live:
        while True:
            try:
                cpu = get_cpu_percent()
                mem = get_memory_percent()
                swap = get_swap_percent()
                disk = get_disk_percent()
                procs = get_top_processes()
                layout = build_dashboard(cpu, mem, swap, disk, procs)
                live.update(layout)
                time.sleep(args.interval)
            except KeyboardInterrupt:
                console.print("\n[bold green]Dashboard stopped.[/bold green]")
                return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
