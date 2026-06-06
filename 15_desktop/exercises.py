#!/usr/bin/env python3
"""Desktop exercises: Tkinter windows, layouts, event binding, MVC pattern, Notebook tabs."""

import tkinter as tk
from tkinter import ttk

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 1: Basic Tkinter window with label and button
# ═══════════════════════════════════════════════════════════════════════════════

# NOTE: No mainloop() call — just the setup pattern.
# To run: remove the comment on root.mainloop()

root1 = tk.Tk()
root1.title("Exercise 1 — Basic Window")
root1.geometry("300x150")

label1 = tk.Label(root1, text="Hello, Tkinter!", font=("Helvetica", 16))
label1.pack(pady=10)

def on_click():
    """Update label text when button is clicked."""
    label1.config(text="Button was clicked!")

btn1 = tk.Button(root1, text="Click Me", command=on_click)
btn1.pack(pady=5)

print("Exercise 1 — Basic window created (not shown):")
print(f"  Title: {root1.title()}")
print(f"  Geometry: {root1.geometry()}")
print(f"  Widgets: Label + Button with callback")
# root1.mainloop()  # uncomment to run interactively
root1.destroy()  # clean up
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 2: Tkinter layout — grid vs pack vs place comparison
# ═══════════════════════════════════════════════════════════════════════════════

root2 = tk.Tk()
root2.title("Exercise 2 — Layouts")
root2.geometry("450x250")

# --- Grid layout (left frame) ---
grid_frame = tk.LabelFrame(root2, text="Grid Layout", padx=5, pady=5)
grid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

# Grid arranges widgets in rows/columns — best for forms
tk.Label(grid_frame, text="Username:").grid(row=0, column=0, sticky="e", pady=2)
tk.Entry(grid_frame).grid(row=0, column=1, pady=2)
tk.Label(grid_frame, text="Password:").grid(row=1, column=0, sticky="e", pady=2)
tk.Entry(grid_frame, show="*").grid(row=1, column=1, pady=2)
tk.Button(grid_frame, text="Login").grid(row=2, column=0, columnspan=2, pady=5)

# --- Pack layout (right frame) ---
pack_frame = tk.LabelFrame(root2, text="Pack Layout", padx=5, pady=5)
pack_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

# Pack stacks widgets side-by-side or top-to-bottom — best for toolbars/sidebars
tk.Label(pack_frame, text="Toolbar", bg="lightgray").pack(fill=tk.X)
tk.Button(pack_frame, text="New").pack(side=tk.LEFT, padx=2)
tk.Button(pack_frame, text="Open").pack(side=tk.LEFT, padx=2)
tk.Button(pack_frame, text="Save").pack(side=tk.LEFT, padx=2)
tk.Label(pack_frame, text="\nPlace sets exact x,y coordinates —\nrarely used, avoid if possible.").pack(pady=10)

print("Exercise 2 — Layout comparison built:")
print("  Grid:    row/column positioning — ideal for forms")
print("  Pack:    side-by-side or top-to-bottom — ideal for toolbars")
print("  Place:   absolute x,y coordinates — avoid for responsive UIs")
# root2.mainloop()
root2.destroy()
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 3: Tkinter event binding — keypresses and button clicks
# ═══════════════════════════════════════════════════════════════════════════════

root3 = tk.Tk()
root3.title("Exercise 3 — Event Binding")
root3.geometry("350x200")

event_log: list[str] = []

def log_event(description: str, event: "tk.Event | None" = None):
    """Record event details and update display."""
    detail = description
    if event:
        detail += f" (char={getattr(event, 'char', '?')}, keysym={getattr(event, 'keysym', '?')})"
    event_log.append(detail)
    # Keep only last 5 events
    if len(event_log) > 5:
        event_log.pop(0)
    status_var.set("\n".join(event_log))

status_var = tk.StringVar(value="Press keys or click buttons...")

# Status label showing recent events
status_label = tk.Label(
    root3, textvariable=status_var, justify=tk.LEFT,
    bg="white", relief=tk.SUNKEN, anchor="nw", padx=5, pady=5
)
status_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Button with click binding
btn_frame = tk.Frame(root3)
btn_frame.pack(pady=5)

btn_ok = tk.Button(btn_frame, text="OK", command=lambda: log_event("OK pressed"))
btn_ok.pack(side=tk.LEFT, padx=5)

btn_cancel = tk.Button(btn_frame, text="Cancel", command=lambda: log_event("Cancel pressed"))
btn_cancel.pack(side=tk.LEFT, padx=5)

# Key bindings on the root window
root3.bind("<KeyPress>", lambda e: log_event(f"Key pressed", e))
root3.bind("<Return>", lambda e: log_event("Enter key", e))
root3.bind("<Escape>", lambda e: log_event("Escape key", e))

# Simulate some events programmatically
root3.event_generate("<KeyPress>", keysym="a")
root3.event_generate("<Return>", keysym="Return")
btn_ok.invoke()  # simulate button click

print("Exercise 3 — Event binding demonstrated:")
print("  Events logged:")
for line in event_log:
    print(f"    {line}")
print("  Bindings: <KeyPress>, <Return>, <Escape>, Button commands")
# root3.mainloop()
root3.destroy()
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 4: MVC pattern — separate Model/View/Controller for a todo item
# ═══════════════════════════════════════════════════════════════════════════════

# --- Model: pure data and business logic, no UI code ---
class TodoModel:
    """Holds todo items and provides operations. No tkinter imports."""

    def __init__(self):
        self._todos: list[dict] = []
        self._observers: list = []  # observers notified on change

    def add_observer(self, callback):
        """Register a callback that fires when the model changes."""
        self._observers.append(callback)

    def _notify(self):
        for cb in self._observers:
            cb()

    def add_todo(self, title: str):
        self._todos.append({"title": title, "done": False})
        self._notify()

    def toggle(self, index: int):
        if 0 <= index < len(self._todos):
            self._todos[index]["done"] = not self._todos[index]["done"]
            self._notify()

    @property
    def todos(self) -> list[dict]:
        return list(self._todos)  # defensive copy

    @property
    def count_done(self) -> int:
        return sum(1 for t in self._todos if t["done"])


# --- View: only rendering, no business logic ---
class TodoView:
    """Renders the todo list into a Listbox. Knows about tkinter but not logic."""

    def __init__(self, parent):
        self.listbox = tk.Listbox(parent, height=6, selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def render(self, todos: list[dict]):
        self.listbox.delete(0, tk.END)
        for i, t in enumerate(todos):
            mark = "✅" if t["done"] else "⬜"
            self.listbox.insert(tk.END, f"{mark} {t['title']}")


# --- Controller: mediates between model and view ---
class TodoController:
    """Wires model ↔ view, handles user actions."""

    def __init__(self, model: TodoModel, view: TodoView):
        self.model = model
        self.view = view
        self.model.add_observer(self.refresh)

    def refresh(self):
        self.view.render(self.model.todos)

    def add_todo(self, title: str):
        self.model.add_todo(title)

    def toggle_selected(self):
        selection = self.view.listbox.curselection()
        if selection:
            self.model.toggle(selection[0])


# Build MVC in a window
root4 = tk.Tk()
root4.title("Exercise 4 — MVC Todo")
root4.geometry("300x250")

model = TodoModel()
view = TodoView(root4)
controller = TodoController(model, view)

# Input frame
input_frame = tk.Frame(root4)
input_frame.pack(fill=tk.X, padx=5, pady=5)

entry = tk.Entry(input_frame)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

def add_todo_action():
    if entry.get().strip():
        controller.add_todo(entry.get())
    entry.delete(0, tk.END)

add_btn = tk.Button(input_frame, text="Add", command=add_todo_action)
add_btn.pack(side=tk.RIGHT)

toggle_btn = tk.Button(
    root4,
    text="Toggle Done",
    command=controller.toggle_selected,
)
toggle_btn.pack(pady=5)

# Simulate usage
controller.add_todo("Buy groceries")
controller.add_todo("Walk the dog")
controller.add_todo("Read a book")
controller.model.toggle(0)  # mark first as done

print("Exercise 4 — MVC Todo pattern:")
print(f"  Todos: {model.todos}")
print(f"  Done count: {model.count_done}")
print("  Architecture: Model (data) → View (Listbox) ← Controller (wires events)")
# root4.mainloop()
root4.destroy()
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# BONUS: Tkinter ttk.Notebook with multiple tabs
# ═══════════════════════════════════════════════════════════════════════════════

root5 = tk.Tk()
root5.title("BONUS — ttk.Notebook Tabs")
root5.geometry("400x300")

# Notebook is the tab container
notebook = ttk.Notebook(root5)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- Tab 1: General settings ---
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="General")
ttk.Label(tab1, text="Application Settings", font=("Helvetica", 12)).pack(pady=10)
ttk.Checkbutton(tab1, text="Enable dark mode").pack(anchor="w", padx=20)
ttk.Checkbutton(tab1, text="Start on boot").pack(anchor="w", padx=20)
ttk.Checkbutton(tab1, text="Send analytics").pack(anchor="w", padx=20)

# --- Tab 2: Network settings ---
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Network")
ttk.Label(tab2, text="Network Configuration", font=("Helvetica", 12)).pack(pady=10)
ttk.Label(tab2, text="Host:").pack(anchor="w", padx=20)
ttk.Entry(tab2).pack(fill=tk.X, padx=20, pady=2)
ttk.Label(tab2, text="Port:").pack(anchor="w", padx=20)
ttk.Entry(tab2).pack(fill=tk.X, padx=20, pady=2)

# --- Tab 3: About ---
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="About")
ttk.Label(
    tab3,
    text="MyApp v2.0\n\nBuilt with Python + Tkinter\n\n"
         "© 2026 Acme Corp",
    font=("Helvetica", 10),
    justify=tk.CENTER,
).pack(expand=True)

print("BONUS — ttk.Notebook with 3 tabs:")
for tab_id in notebook.tabs():
    tab_name = notebook.tab(tab_id, "text")
    print(f"  Tab: {tab_name}")
# root5.mainloop()
root5.destroy()
print("---")

print("All desktop exercises passed.")
