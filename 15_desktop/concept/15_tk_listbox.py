#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk


def add_item():
    if item := entry.get():
        listbox.insert(tk.END, item)
        result_label.config(text=f"Added Item: {item}")
        entry.delete(0, tk.END)


def remove_selected_items():
    selected_indices = listbox.curselection()
    removed_items = [listbox.get(idx) for idx in selected_indices]
    for idx in reversed(selected_indices):
        listbox.delete(idx)
    if removed_items:
        result_label.config(text=f"Deleted Items: {', '.join(removed_items)}")
    else:
        result_label.config(text="No item selected to delete")


# Create the main window
root = tk.Tk()
root.title("Multi-Selection Listbox")

# Create a Combobox-like entry field
entry = ttk.Entry(root)
entry.grid(row=0, column=0, padx=10, pady=10)

# Create a Listbox to display selected items
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
listbox.grid(row=1, column=0, padx=10, pady=10)

# Create buttons for adding and removing items
add_button = ttk.Button(root, text="Add Item", command=add_item)
add_button.grid(row=0, column=1, padx=10, pady=10)

remove_button = ttk.Button(root, text="Remove Selected", command=remove_selected_items)
remove_button.grid(row=1, column=1, padx=10, pady=10)

# Create a label to display selected items
result_label = ttk.Label(root, text="")
result_label.grid(row=3, column=0, padx=0, pady=10)

# Run the Tkinter main loop
root.mainloop()
