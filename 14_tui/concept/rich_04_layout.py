#!/usr/bin/env python3
# rich: Panel, Columns, Console.rule, layout helpers, text alignment
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.table import Table
from rich import box

console = Console(width=80)

# --- Console.rule: a horizontal rule with optional title ---
console.rule("[bold green]Section 1: Panels")
console.print()

# --- Panel: draw a border around content ---
panel_text = Text.from_markup(
    "Rich provides [bold cyan]Panels[/bold cyan] to wrap content in a bordered box.\n"
    "You can customize the [yellow]border style[/yellow] and [magenta]title[/magenta]."
)
panel = Panel(
    panel_text,
    title="Information",
    subtitle="v1.0",
    border_style="blue",
    box=box.ROUNDED,
    padding=(1, 2),
)
console.print(panel)
console.print()

# --- Panels with different box styles ---
box_styles = [
    ("ASCII", box.ASCII),
    ("SQUARE", box.SQUARE),
    ("ROUNDED", box.ROUNDED),
    ("HEAVY", box.HEAVY),
    ("DOUBLE", box.DOUBLE),
]
panels = [
    Panel(f"[bold]{name}[/bold]", box=style, border_style="cyan")
    for name, style in box_styles
]
console.print(Columns(panels))
console.print()

# --- Columns: side-by-side layout ---
console.rule("[bold green]Section 2: Columns Layout")
console.print()

# Columns with equal widths
left = Panel("Left column\nContent here", title="Left", border_style="red")
middle = Panel("Middle column\nMore content", title="Middle", border_style="green")
right = Panel("Right column\nEven more", title="Right", border_style="yellow")

console.print(Columns([left, middle, right]))
console.print()

# --- Columns with a table inside a Panel ---
console.rule("[bold green]Section 3: Nested Layout")
console.print()

stats_table = Table(show_header=False, box=box.SIMPLE)
stats_table.add_column(style="cyan")
stats_table.add_column(justify="right")
stats_table.add_row("CPU", "45%")
stats_table.add_row("Memory", "8.2 GB")
stats_table.add_row("Disk", "120 GB")

dashboard = Panel(
    stats_table,
    title="[bold]System Monitor[/bold]",
    border_style="green",
    box=box.HEAVY,
)
console.print(dashboard)
console.print()

# --- Pad and alignment ---
console.rule("[bold green]Section 4: Text Alignment")
padded = Panel("  Centered text with padding  ", style="bold yellow", width=40)
console.print(padded, justify="center")
