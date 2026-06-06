#!/usr/bin/env python3
"""Full CLI todo manager — add, list, done, delete.  JSON file storage, argparse subparsers."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


TODO_FILE = Path(os.environ.get("TODO_FILE", Path.home() / ".todos.json"))


def load_todos() -> List[dict]:
    if TODO_FILE.exists():
        with open(TODO_FILE) as f:
            return json.load(f)
    return []


def save_todos(todos: List[dict]) -> None:
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------
def cmd_add(args: argparse.Namespace) -> int:
    todos = load_todos()
    task = {
        "id": (max((t["id"] for t in todos), default=0) + 1),
        "title": args.title,
        "done": False,
        "created": datetime.now().isoformat(timespec="seconds"),
    }
    todos.append(task)
    save_todos(todos)
    print(f"Added #{task['id']}: {task['title']}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    todos = load_todos()
    if not todos:
        print("No todos yet. Use 'add' to create one.")
        return 0

    filtered = [t for t in todos if not t["done"]] if not args.all else todos
    if not filtered:
        print("All done!")
        return 0

    for t in filtered:
        marker = "[x]" if t["done"] else "[ ]"
        print(f"  {marker} #{t['id']:>3}  {t['title']}  ({t.get('created','')})")
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    todos = load_todos()
    found: Optional[dict] = None
    for t in todos:
        if t["id"] == args.id:
            found = t
            break
    if found is None:
        print(f"Todo #{args.id} not found.", file=sys.stderr)
        return 1
    found["done"] = True
    found["completed"] = datetime.now().isoformat(timespec="seconds")
    save_todos(todos)
    print(f"Marked #{args.id} as done: {found['title']}")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    todos = load_todos()
    before = len(todos)
    todos = [t for t in todos if t["id"] != args.id]
    if len(todos) == before:
        print(f"Todo #{args.id} not found.", file=sys.stderr)
        return 1
    # Re-index
    for i, t in enumerate(todos, 1):
        t["id"] = i
    save_todos(todos)
    print(f"Deleted #{args.id}.")
    return 0


# ---------------------------------------------------------------------------
# Argparse setup
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="CLI todo manager")
    sub = p.add_subparsers(dest="command", required=True)

    # add
    a = sub.add_parser("add", help="Add a new todo")
    a.add_argument("title", help="Todo title")
    a.set_defaults(func=cmd_add)

    # list
    l = sub.add_parser("list", help="List todos")
    l.add_argument("--all", "-a", action="store_true", help="Include completed")
    l.set_defaults(func=cmd_list)

    # done
    d = sub.add_parser("done", help="Mark a todo as done")
    d.add_argument("id", type=int, help="Numeric todo ID")
    d.set_defaults(func=cmd_done)

    # delete
    rm = sub.add_parser("delete", aliases=["rm"], help="Delete a todo")
    rm.add_argument("id", type=int, help="Numeric todo ID")
    rm.set_defaults(func=cmd_delete)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    exit_code = args.func(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
