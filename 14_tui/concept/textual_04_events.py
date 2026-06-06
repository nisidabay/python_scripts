#!/usr/bin/env python3
# textual: event handling — on_button_pressed, on_key, message handlers
# Press Ctrl+C to exit.

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Input, RichLog
from textual.containers import Horizontal, Vertical
from textual import events
from textual.message import Message


class Counter(Static):
    """A custom widget that emits a custom message when its value changes."""

    value: int = 0

    class Changed(Message):
        """Posted when the counter value changes."""
        def __init__(self, counter: "Counter", value: int) -> None:
            super().__init__()
            self.counter = counter
            self.value = value

    def increment(self) -> None:
        self.value += 1
        self.update(f"Count: {self.value}")
        self.post_message(self.Changed(self, self.value))

    def decrement(self) -> None:
        self.value -= 1
        self.update(f"Count: {self.value}")
        self.post_message(self.Changed(self, self.value))

    def on_mount(self) -> None:
        self.update(f"Count: {self.value}")


class EventsApp(App):
    """Demonstrates event handling in Textual: buttons, keys, custom messages."""

    CSS = """
    Screen {
        layout: vertical;
    }

    Counter {
        text-style: bold;
        color: $accent;
        content-align: center middle;
        height: 3;
        border: solid $accent;
        margin: 1 2;
    }

    Horizontal {
        height: auto;
        align-horizontal: center;
        margin: 1 0;
    }

    Button {
        margin: 0 1;
        min-width: 10;
    }

    #key-log {
        height: 1fr;
        border: solid $secondary;
        background: $surface;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        # Custom counter widget
        yield Counter()

        # Buttons to manipulate the counter
        with Horizontal():
            yield Button("➕ Increment", id="inc", variant="success")
            yield Button("➖ Decrement", id="dec", variant="warning")
            yield Button("🔄 Reset", id="reset", variant="primary")

        # Key-press log
        yield Static("Press any key... (arrow keys, letters, etc.)", id="key-hint")
        yield RichLog(id="key-log", highlight=True, markup=True)

        yield Footer()

    # --- Built-in event handlers ---
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Respond to button presses."""
        counter = self.query_one(Counter)
        if event.button.id == "inc":
            counter.increment()
        elif event.button.id == "dec":
            counter.decrement()
        elif event.button.id == "reset":
            counter.value = 0
            counter.update("Count: 0")

    def on_key(self, event: events.Key) -> None:
        """Called on every key press — shows all keys."""
        log = self.query_one("#key-log", RichLog)
        log.write(f"[dim]key=[/dim][bold cyan]{event.key!r}[/] "
                  f"[dim]char=[/dim][bold yellow]{event.character!r}[/] "
                  f"[dim]name=[/dim]{event.name}")

        # Arrow keys can also control the counter
        counter = self.query_one(Counter)
        if event.key == "up":
            counter.increment()
            self.query_one("#key-hint", Static).update("↑ Up arrow → increment")
        elif event.key == "down":
            counter.decrement()
            self.query_one("#key-hint", Static).update("↓ Down arrow → decrement")

    # --- Custom message handler ---
    def on_counter_changed(self, event: Counter.Changed) -> None:
        """Respond to our custom Counter.Changed message."""
        log = self.query_one("#key-log", RichLog)
        log.write(f"[bold green]Counter changed: {event.value}[/] (from {event.counter!r})")

    def on_mount(self) -> None:
        self.title = "Textual Events Demo"


if __name__ == "__main__":
    EventsApp().run()
