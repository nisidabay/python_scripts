# Desktop Applications — Tkinter GUIs and MVC architecture pattern

## Quick Start
```bash
# Tkinter Listbox with add/remove (gui, opens window)
python 15_tk_listbox.py

# Full-featured TODO app with SQLite persistence (gui, opens window)
python 15_tk_todo.py

# MVC pattern: Factory for UI element creation
python model_view_controller/Factory3.py

# MVC pattern: Person model + CLI view
python model_view_controller/model.py
python model_view_controller/view.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `15_tk_listbox.py` | Tkinter basics: widgets, grid layout, event callbacks | `tk.Listbox(selectmode=MULTIPLE)`, `ttk.Entry` + `ttk.Button`, `command=` bindings, `.curselection()` / `.get(idx)` |
| `15_tk_todo.py` | Full CRUD app: sqlite3 persistence, canvas scrolling, mouse wheel, alternating row colors | `class Todo(tk.Tk)`, `sqlite3.connect/execute`, `tk.Canvas` scrolling with `Scrollbar`, `event.delta` handling |
| `model_view_controller/model.py` | Data layer: Person dataclass loading from JSON | `@dataclass Person`, `@classmethod create()` reading `json.load()`, separation of data from presentation |
| `model_view_controller/view.py` | Presentation layer: display functions that never touch data logic | Standalone `showAllView(list)`, `startView()`, `endView()` — pure output functions |
| `model_view_controller/Factory3.py` | Factory pattern: dynamic object creation from string type | `ButtonFactory.create_button(kind)` → `globals()[targetclass]()`, polymorphic `get_html()` |

> **Files:** 5 files across `model_view_controller/` and top-level concept directory. Also includes a full `project/rptodo/` CLI app in the parent `15_desktop/` directory.

## Common Patterns
```python
# Tkinter: basic grid layout with callbacks
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
entry = ttk.Entry(root)
entry.grid(row=0, column=0)
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
listbox.grid(row=1, column=0)

def add_item():
    item = entry.get()
    if item:
        listbox.insert(tk.END, item)
        entry.delete(0, tk.END)

ttk.Button(root, text="Add", command=add_item).grid(row=0, column=1)
root.mainloop()

# Tkinter: subclassing root for complex apps
class Todo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.title("To-Do App")
        self.geometry("300x400")
        # Build UI in constructor

# MVC: model layer
from dataclasses import dataclass
import json

@dataclass
class Person:
    first_name: str = ""
    last_name: str = ""

    @classmethod
    def create(cls):
        with open("db.json") as f:
            return [cls(**item) for item in json.load(f)["Persons"]]

# Factory pattern
class ButtonFactory:
    @staticmethod
    def create_button(kind):
        return globals()[kind.capitalize()]()
```

## Now Build Your Own
**Challenge:** Build a Tkinter "Note Pad" app with a `tk.Text` widget for content, a `ttk.Entry` for filename, and Save/Load buttons. Save notes as `.txt` files to a `notes/` directory. Populate a `tk.Listbox` showing all saved files — clicking one loads it into the text area. Use grid layout with the listbox on the left and editor on the right. Add a Delete button.
