#!/usr/bin/python3
from rich import print
from rich.console import Console
from rich.text import Text
from rich.theme import Theme
from rich.traceback import install
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import track
import time

# Neccesary for traceback messages
install()

###############################################################################
# colorized output
print(['a', 1, 2, ("bob", "alice")])

###############################################################################

console = Console()

console.print("Plain text")
console.print("Bold text", style="bold")
console.print("Bold underline", style="bold underline green")
console.print("Bold underline red on white",
              style="bold underline red on white")
console.print("[bold]This is bold [cyan] this cyan[/]")

###############################################################################

text = Text("Hola Carlos")
text.stylize("bold yellow", 0, 4)
console.print(text)
###############################################################################

custom_theme = Theme({"success": "green", "failure": "red"})
console = Console(theme=custom_theme)
console.print("worked", style="success")
console.print("failed", style="failure")
###############################################################################

console.print(":thumbs_up: file downloaded")
console.print(":apple: :bug:")
###############################################################################

for i in range(5):
    console.log("Doing something useless")


def sum(a: int, b: int) -> int:
    console.log("Adding two numbers, log_locals=True")
    return x + y


console = Console()
# Uncomment this to show the demo.html log file
#sum(2 + "a")

###############################################################################

# console = Console(record=True)
#
# try:
# sum(1, 2)
# sum(1, 3)
# sum(1, "a")
# except:
# console.print_exception()
#
# console.save_html("demo.html")
###############################################################################

table = Table(title="Star Wars Movies")
table.add_column("Released", style="cyan")
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="Green")

table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker",
              "$952,110,690")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393, 151,347")
table.add_row("Dec 15, 2017", "Star Wars: The Last Jedi", "$752,110,690")

console = Console()
console.print(table)

###############################################################################
MARKDOWN = """
# This is an h1

Rich can do a pretty *decent* job of rendering markdown.

1. This is a list item
2. This is another list item
"""
console = Console()
md = Markdown(MARKDOWN)
console.print(md)

# also works in command line
# python -d rich.markdown README.md
###############################################################################
from itertools import count
for i in track(count(1), total=100, description="Processing ..."):
    print(f"working {i}")
    time.sleep(0.2)
    if i == 105:
        break
