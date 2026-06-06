#!/usr/bin/env python3
# textual: Grid, Horizontal, Vertical containers — layout systems
# Press Ctrl+C to exit.

from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Static, Label


class LayoutApp(App):
    """Demonstrates Grid, Horizontal, and Vertical container layouts."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 3 2;            /* 3 columns, 2 rows */
        grid-gutter: 1 2;           /* vertical gutter 1, horizontal 2 */
    }

    .box {
        border: solid $accent;
        padding: 1 2;
        content-align: center middle;
    }

    #nav {
        column-span: 3;             /* span full width */
        height: 3;
        background: $surface;
        border: solid $primary;
    }

    #sidebar {
        row-span: 2;                /* span 2 rows */
        background: $panel;
        border: solid $secondary;
    }

    #main {
        column-span: 2;             /* span 2 columns */
        background: $panel;
        border: solid $success;
    }

    /* Horizontal and Vertical nested inside containers */
    Horizontal {
        height: auto;
        align-horizontal: center;
    }

    .chip {
        width: 12;
        padding: 0 1;
        border: solid $accent;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        with Grid():
            # Navigation bar spans all columns
            with Horizontal(id="nav"):
                yield Static("🏠 Home", classes="chip")
                yield Static("📁 Files", classes="chip")
                yield Static("⚙ Settings", classes="chip")
                yield Static("❓ Help", classes="chip")

            # Sidebar — uses Vertical for stacking
            with Vertical(id="sidebar"):
                yield Static("📋 Sidebar", classes="box")
                yield Static("• Item One")
                yield Static("• Item Two")
                yield Static("• Item Three")
                yield Static("• Item Four")
                yield Static("• Item Five")

            # Main area
            with Vertical(id="main"):
                yield Static("📄 Main Content Area", classes="box")
                yield Static("This area would contain the primary content.")
                yield Static("Use Vertical/Horizontal containers to structure widgets.")

        yield Footer()


if __name__ == "__main__":
    LayoutApp().run()
