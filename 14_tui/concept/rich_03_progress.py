#!/usr/bin/env python3
# rich: Progress bar, track() helper, Spinner context manager, columns of progress
import time
from rich.console import Console
from rich.progress import (
    Progress, SpinnerColumn, BarColumn, TextColumn,
    TimeElapsedColumn, TimeRemainingColumn, track
)
from rich.live import Live

console = Console()

# --- track(): simple progress bar for iterables ---
console.print("[bold]track() — simple loop progress[/bold]")
for i in track(range(20), description="Processing items..."):
    time.sleep(0.05)  # simulate work
console.print()

# --- Progress with custom columns ---
console.print("[bold]Custom Progress bar[/bold]")
with Progress(
    SpinnerColumn(),              # spinning indicator
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),                  # the actual bar
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
    console=console,
) as progress:
    task = progress.add_task("[cyan]Downloading...", total=100)

    while not progress.finished:
        progress.update(task, advance=0.8)
        time.sleep(0.02)

console.print()

# --- Multiple parallel progress bars ---
console.print("[bold]Multiple parallel tasks[/bold]")
with Progress(
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    console=console,
) as progress:
    task1 = progress.add_task("[red]Task A", total=50)
    task2 = progress.add_task("[green]Task B", total=30)
    task3 = progress.add_task("[yellow]Task C", total=70)

    for _ in range(70):
        progress.update(task1, advance=1)
        if _ < 30:
            progress.update(task2, advance=1)
        if _ < 70:
            progress.update(task3, advance=0.8)
        time.sleep(0.03)

console.print()

# --- Manual progress bar (no context manager) ---
console.print("[bold]Manual progress[/bold]")
progress = Progress(console=console)
task_id = progress.add_task("Manual...", total=50)
progress.start()
for _ in range(50):
    time.sleep(0.01)
    progress.update(task_id, advance=1)
progress.stop()
console.print("Done!\n")

# --- SpinnerColumn as a standalone context ---
console.print("[bold]Spinner while working[/bold]")
with console.status("[bold green]Thinking deeply...", spinner="dots"):
    time.sleep(1.5)  # simulate long computation
console.print("Thought complete!")
