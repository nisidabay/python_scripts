# Terminal User Interfaces — Rich formatting library + Textual TUI framework + Urwid

## Quick Start
```bash
pip install rich textual urwid pygame    # dependencies

# === Rich Library ===
# Colorized output, markdown, tables, tracebacks
python 14_rich_basics.py

# Rich Tables with columns, styles, footers
python rich_02_tables.py

# Rich Progress bars: track(), multi-bar, spinner
python rich_03_progress.py

# Rich Layout: Panel, Columns, Console.rule, box styles
python rich_04_layout.py

# Rich Live display: auto-refreshing tables, counters, spinners
python rich_05_live.py

# === Textual Framework ===
# Minimal app with Header/Footer/Static
python textual_01_hello.py

# Grid layout: Horizontal, Vertical, scrollable containers
python textual_02_layout.py

# Widgets: Button, Input, Label, event handling
python textual_03_widgets.py

# Events: custom widgets, key handling, custom messages
python textual_04_events.py

# === Urwid ===
# Terminal music player (urwid UI + pygame backend)
python 14_urwid_player.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `14_rich_basics.py` | Rich fundamentals: colored print, Text styling, themes, tables, markdown, traceback, progress | `from rich import print`, `Console()`, `Text().stylize()`, `Theme()`, `install()` for tracebacks |
| `rich_02_tables.py` | Table with add_column/add_row, Column objects, footer rows, section breaks | `Table(title=…)`, `Column("name", style=…)`, `.add_section()`, styled footer row |
| `rich_03_progress.py` | Progress bars: track(), custom columns, multi-task, manual mode, spinner context | `track(iter, description=)`, `Progress(SpinnerColumn, BarColumn, TextColumn)`, `console.status()` |
| `rich_04_layout.py` | Layout: Panel, Columns, Console.rule, box border styles, nested tables | `Panel(content, title=, border_style=)`, `Columns([left, middle, right])`, import `box` for styles |
| `rich_05_live.py` | Live display: auto-refreshing tables, text counters, spinner stages | `with Live(table, refresh_per_second=4)`, `live.update(new_content)` in loop |
| `textual_01_hello.py` | Textual app structure: App subclass, compose(), CSS, widget tree | `class HelloApp(App)`, `def compose() → yield Header/Footer/Static`, inline CSS string |
| `textual_02_layout.py` | Grid layout with column/row spans, Horizontal/Vertical containers | `grid-size: 3 2;`, `column-span: 3;`, nested `Horizontal(id="nav")`, `Vertical(id="sidebar")` |
| `textual_03_widgets.py` | Button variants, Input, Label, ScrollableContainer, event handlers | `Button("label", variant="primary")`, `on_button_pressed()`, `self.query_one("#id", WidgetType)` |
| `textual_04_events.py` | Custom widgets, custom messages, key events, RichLog output | `class Counter(Static)` with `class Changed(Message)`, `on_key()`, `RichLog` for logging |
| `14_urwid_player.py` | Full terminal music player with Urwid UI | `urwid.MainLoop`, `Frame`/`Pile`/`Columns` layout, `urwid.Button`, progress bar, background threads |

> **Files:** 10 files (5 Rich, 4 Textual, 1 Urwid).

## Common Patterns
```python
# Rich: colored terminal output
from rich.console import Console
from rich.table import Table
console = Console()
table = Table(title="Title")
table.add_column("Col1", style="cyan")
table.add_row("Value")
console.print(table)

# Rich: progress bar
from rich.progress import track
for item in track(items, description="Processing..."):
    process(item)

# Rich: live updating display
from rich.live import Live
with Live(table, refresh_per_second=4) as live:
    for data in stream:
        live.update(build_table(data))

# Textual: minimal app
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
class MyApp(App):
    CSS = "Screen { align: center middle; }"
    def compose(self) -> ComposeResult:
        yield Header(); yield Static("Hello!"); yield Footer()
MyApp().run()

# Textual: event handling
def on_button_pressed(self, event: Button.Pressed) -> None:
    self.query_one("#output", Static).update("Clicked!")
```

## Now Build Your Own
**Challenge:** Build a Textual dashboard app with three panels: a Rich-based header (use `rich.Text`), a live-updating counter in the center, and a footer showing keyboard shortcuts. Track key presses and display the last 10 in a scrollable log panel. Use Grid layout with a 3-column header and 2-column body (sidebar + main).
