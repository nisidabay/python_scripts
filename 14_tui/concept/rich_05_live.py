#!/usr/bin/env python3
# rich: Live display — refreshable, auto-updating terminal output
import time
import random
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout

console = Console()

# --- Live-updating table ---
console.print("[bold]Live-updating monitoring table[/bold]")
console.print()

table = Table(title="Server Metrics")
table.add_column("Metric")
table.add_column("Value", justify="right")
table.add_column("Status")

servers = ["web-01", "web-02", "db-master", "cache-01"]

with Live(table, console=console, refresh_per_second=4, vertical_overflow="visible") as live:
    for step in range(20):
        # Rebuild the table fresh each iteration
        table = Table(title="Server Metrics")
        table.add_column("Metric")
        table.add_column("Value", justify="right")
        table.add_column("Status")

        for server in servers:
            cpu = random.randint(5, 95)
            mem = random.randint(20, 90)
            lat = random.randint(1, 500)

            cpu_status = "[red]HIGH" if cpu > 80 else "[green]OK"
            mem_status = "[red]HIGH" if mem > 80 else "[green]OK"
            lat_status = "[red]SLOW" if lat > 300 else "[green]OK"

            table.add_row(f"{server} CPU", f"{cpu}%", cpu_status)
            table.add_row(f"{server} MEM", f"{mem}%", mem_status)
            table.add_row(f"{server} LAT", f"{lat}ms", lat_status)
            table.add_section()

        live.update(table)
        time.sleep(0.2)

console.print()

# --- Live-updating text (progress counter) ---
console.print("[bold]Live text counter[/bold]")
with Live(console=console, refresh_per_second=10) as live:
    for i in range(30):
        color = "green" if i < 15 else "yellow" if i < 25 else "red"
        live.update(
            Panel(
                Text(f"Downloading... {i+1}/30 files", style=f"bold {color}"),
                border_style=color,
            )
        )
        time.sleep(0.05)
    live.update(Panel("[bold green]✓ Complete![/bold green]", border_style="green"))

console.print()

# --- Live spinner with changing status ---
console.print("[bold]Live spinner status[/bold]")
with Live(
    Panel("Starting...", border_style="cyan"),
    console=console,
    refresh_per_second=4,
) as live:
    stages = ["Connecting", "Authenticating", "Fetching data", "Processing", "Done!"]
    for stage in stages:
        live.update(
            Panel(
                Text(stage, style="bold yellow"),
                border_style="yellow",
                title="[bold cyan]Worker[/bold cyan]",
            )
        )
        time.sleep(0.4)
    live.update(Panel("[bold green]✓ All tasks complete[/bold green]", border_style="green"))
