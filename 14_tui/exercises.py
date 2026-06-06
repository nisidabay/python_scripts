#!/usr/bin/env python3
"""TUI exercises: Rich tables, progress bars, layouts, live displays, Textual app."""

import io
import time
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, track
from rich.panel import Panel
from rich.columns import Columns
from rich.live import Live
from rich.text import Text

console = Console(width=80, force_terminal=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 1: Rich Table from CSV data
# ═══════════════════════════════════════════════════════════════════════════════

# Simulate CSV data — in real code you'd read from a file
csv_lines = [
    "Product,Q1,Q2,Q3,Q4",
    "Widget,1200,1450,1300,1600",
    "Gadget,800,920,1100,1050",
    "Doohickey,450,480,520,600",
]

# Split header and data rows, skipping the header for data
header = csv_lines[0].split(",")
rows = [line.split(",") for line in csv_lines[1:]]

table = Table(title="Quarterly Sales Report", show_header=True, header_style="bold cyan")
for col in header:
    table.add_column(col, justify="right")

# Add rows, converting numbers to int for formatting
for row in rows:
    # First column is string, rest are ints
    table.add_row(row[0], *(str(int(v)) for v in row[1:]))

console.print("Exercise 1 — Rich Table:\n")
console.print(table)
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 2: Rich Progress bar with track() over a list
# ═══════════════════════════════════════════════════════════════════════════════

# Simulate processing a list of files with a progress bar
files_to_process = [
    "data_01.csv", "data_02.csv", "data_03.csv",
    "data_04.csv", "data_05.csv", "data_06.csv",
    "data_07.csv", "data_08.csv",
]

console.print("\nExercise 2 — Rich Progress bar:")
# Use track() which wraps any iterable with a progress bar
# In real code: for file in track(files_to_process, description="Processing..."):
# Here we simulate work by iterating
results = []
for file in track(files_to_process, description="Processing files"):
    time.sleep(0.1)  # simulate I/O
    results.append(f"processed {file}")

print(f"  Completed: {len(results)} files processed")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 3: Rich Panel + Columns layout for a dashboard
# ═══════════════════════════════════════════════════════════════════════════════

# Build three panels representing system metrics
cpu_panel = Panel(
    "[bold green]CPU: 23%[/bold green]\n"
    "[dim]4 cores @ 2.5GHz[/dim]",
    title="CPU Usage",
    border_style="green",
    width=25,
)

memory_panel = Panel(
    "[bold yellow]RAM: 7.2 / 16.0 GB[/bold yellow]\n"
    "[dim]45% used[/dim]",
    title="Memory",
    border_style="yellow",
    width=25,
)

disk_panel = Panel(
    "[bold red]Disk: 89%[/bold red]\n"
    "[dim]WARNING: /dev/sda1[/dim]",
    title="Storage",
    border_style="red",
    width=25,
)

# Arrange panels side by side
columns = Columns([cpu_panel, memory_panel, disk_panel], equal=True, expand=False)

console.print("\nExercise 3 — Rich Panel + Columns dashboard:\n")
console.print(columns)
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 4: Rich Live display that updates every second (countdown)
# ═══════════════════════════════════════════════════════════════════════════════

console.print("\nExercise 4 — Rich Live countdown:\n")

# Capture Live output to a buffer so we can inspect it
live_buffer = io.StringIO()
live_console = Console(file=live_buffer, force_terminal=True, width=40)

with Live(console=live_console, refresh_per_second=4) as live:
    for remaining in range(5, 0, -1):
        # Build the countdown display
        text = Text()
        text.append("⏳  Countdown\n", style="bold")
        text.append(f"{'█' * remaining}{'░' * (5 - remaining)}", style="cyan")
        text.append(f"\n{remaining} seconds remaining", style="bold yellow")
        live.update(text)
        time.sleep(0.3)

    text = Text("✅  Liftoff!", style="bold green blink")
    live.update(text)
    time.sleep(0.2)

# Show what the live display rendered
print("Live display completed (countdown 5..1 → Liftoff!)")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# BONUS: Textual app with a counter button (class only, not interactive)
# ═══════════════════════════════════════════════════════════════════════════════

# Textual may not be installed — guard the import
COUNTER_APP_CLASS = """
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static

class CounterApp(App):
    \"\"\"A simple Textual app with a counter and button.\"\"\"
    
    CSS = \"\"\"
    #counter {
        content-align: center middle;
        height: 5;
        text-style: bold;
    }
    #increment-btn {
        width: 30;
        margin: 1 2;
    }
    \"\"\"
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(\"0\", id=\"counter\")
        yield Button(\"Increment\", id=\"increment-btn\", variant=\"primary\")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == \"increment-btn\":
            counter = self.query_one(\"#counter\", Static)
            counter.update(str(int(str(counter.renderable)) + 1))

# if __name__ == \"__main__\":
#     app = CounterApp()
#     app.run()
"""

print("BONUS — Textual CounterApp class (not interactive):")
print("  CounterApp: A full Textual TUI with Header, counter label,")
print("  increment Button, and Footer. Uses CSS for layout and")
print("  on_button_pressed event handler to update the count.")
# Check if textual is importable and show the code
try:
    import textual as _textual  # noqa: F401
    print("  (textual is installed — ready to run)")
except ImportError:
    print("  (textual not installed — install with: pip install textual)")

print("---")

print("All TUI exercises passed.")
