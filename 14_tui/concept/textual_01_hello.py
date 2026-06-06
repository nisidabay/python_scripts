#!/usr/bin/env python3
# textual: minimal App with compose() and a basic widget
# Run with: python textual_01_hello.py
# Press Ctrl+C to exit.

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static


class HelloApp(App):
    """A minimal Textual application demonstrating compose() and static text."""

    CSS = """
    Screen {
        align: center middle;
    }
    Static#greeting {
        text-style: bold;
        color: cyan;
        width: auto;
        height: auto;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        """Build the widget tree — called once on startup."""
        yield Header(show_clock=True)        # built-in header bar with clock
        yield Static("Hello, Textual! 👋\n\nPress Ctrl+C to quit", id="greeting")
        yield Footer()                        # built-in footer with keybindings

    def on_mount(self) -> None:
        """Called after compose, when the app is fully mounted."""
        self.title = "Textual Hello World"
        self.sub_title = "A minimal example"


if __name__ == "__main__":
    app = HelloApp()
    app.run()
