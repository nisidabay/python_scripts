#!/usr/bin/env python3
# textual: Button, Input, Static, Header, Footer widgets
# Press Ctrl+C to exit.

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Input, Label
from textual.containers import Horizontal, Vertical, ScrollableContainer


class WidgetsApp(App):
    """Showcase of core Textual widgets: Button, Input, Static, Label."""

    CSS = """
    Screen {
        layout: vertical;
    }

    #output-area {
        height: 1fr;
        border: solid $secondary;
        background: $surface;
        padding: 1 2;
    }

    Horizontal {
        height: auto;
        align-horizontal: center;
        margin: 1 0;
    }

    Button {
        margin: 0 1;
    }

    #counter-display {
        text-style: bold;
        color: $success;
        content-align: center middle;
        height: 3;
    }

    Input {
        margin: 0 1;
    }

    Label {
        margin: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        # --- Button row ---
        with Horizontal():
            yield Label("Buttons:")
            yield Button("Primary", variant="primary", id="btn-primary")
            yield Button("Success", variant="success", id="btn-success")
            yield Button("Warning", variant="warning", id="btn-warning")
            yield Button("Error", variant="error", id="btn-error")
            yield Button("Default", id="btn-default")

        yield Static("", id="counter-display")

        # --- Input row ---
        with Horizontal():
            yield Label("Name:")
            yield Input(placeholder="Type your name...", id="name-input")
            yield Button("Greet", id="btn-greet")

        # --- Output area ---
        with ScrollableContainer(id="output-area"):
            yield Static("Output will appear here...\n", id="output-log")

        yield Footer()

    # --- Event handlers ---
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle all button presses."""
        btn_id = event.button.id
        output = self.query_one("#output-log", Static)

        if btn_id == "btn-primary":
            output.update(f"{output.renderable}\n[Primary button] Pressed!")
        elif btn_id == "btn-success":
            output.update(f"{output.renderable}\n[Success button] Operation completed ✓")
        elif btn_id == "btn-warning":
            output.update(f"{output.renderable}\n[Warning button] Proceed with caution ⚠")
        elif btn_id == "btn-error":
            output.update(f"{output.renderable}\n[Error button] Something went wrong ✗")
        elif btn_id == "btn-default":
            output.update(f"{output.renderable}\n[Default button] Clicked.")
        elif btn_id == "btn-greet":
            name_input = self.query_one("#name-input", Input)
            name = name_input.value.strip() or "Stranger"
            output.update(f"{output.renderable}\nHello, {name}! 👋")
            name_input.clear()

    # Counter demonstration using Static widget
    _count = 0  # type: ignore

    def on_mount(self) -> None:
        self.title = "Textual Widgets Demo"
        self.set_interval(1, self._update_counter)

    def _update_counter(self) -> None:
        self._count += 1
        display = self.query_one("#counter-display", Static)
        display.update(f"App running for {self._count} seconds")


if __name__ == "__main__":
    WidgetsApp().run()
