#!/usr/bin/env python3
# rich: Table with add_column, add_row, styles, and formatting
from rich.console import Console
from rich.table import Table, Column
from rich.text import Text

console = Console()

# --- Basic Table with title ---
table = Table(title="Top Programming Languages 2024")

table.add_column("Rank", style="cyan", justify="right", no_wrap=True)
table.add_column("Language", style="magenta")
table.add_column("Usage %", justify="right", style="green")
table.add_column("Trend", style="yellow")

table.add_row("1", "Python", "28.1%", "↑ +2.3%")
table.add_row("2", "JavaScript", "24.7%", "↓ -0.5%")
table.add_row("3", "Java", "15.8%", "↓ -1.2%")
table.add_row("4", "C++", "11.3%", "→ 0.0%")
table.add_row("5", "TypeScript", "10.5%", "↑ +1.8%")
table.add_row("6", "Go", "9.6%", "↑ +1.1%")

console.print(table)
console.print()

# --- Table with per-column style objects ---
# Using Column() for more control over each column
inventory = Table(
    Column("Item", style="bold cyan"),
    Column("Qty", justify="right", style="green"),
    Column("Price", justify="right", style="yellow"),
    Column("Total", justify="right", style="bold green"),
    title="Inventory",
    caption="[dim]Prices in USD[/dim]",
    show_lines=True,           # horizontal separator between rows
)

items = [
    ("Widget", 50, 3.50),
    ("Gadget", 30, 12.99),
    ("Doohickey", 100, 1.25),
    ("Thingamajig", 15, 27.50),
]
for name, qty, price in items:
    total = qty * price
    inventory.add_row(name, str(qty), f"${price:.2f}", f"${total:.2f}")

# Add a footer row with summary style
inventory.add_section()
inventory.add_row(
    Text("TOTAL", style="bold"),
    str(sum(q for _, q, _ in items)),
    "",
    f"${sum(q * p for _, q, p in items):.2f}",
    style="on grey30",
)

console.print(inventory)
