#!/usr/bin/env python3
# exercises.py — Group 02: CLI Apps
# 4 solved exercises + BONUS. Run: python3 exercises.py
# NOTE: Each exercise simulates CLI args in-process (no interactive input needed).

import argparse
import re
import sys


# ============================================================
# Exercise 1: argparse with --count (int), --prefix (str),
#            positional filename
# ============================================================

def exercise1() -> None:
    """Simulate: python3 script.py data.txt --count 5 --prefix LOG"""
    parser = argparse.ArgumentParser(description="Read a file with options.")
    parser.add_argument("filename", type=str, help="Path to the input file")
    parser.add_argument("--count", type=int, default=1,
                        help="How many lines to read")
    parser.add_argument("--prefix", type=str, default="",
                        help="Prefix to prepend to each line")
    # Simulate CLI args without actually calling sys.argv
    args = parser.parse_args(["data.txt", "--count", "5", "--prefix", "LOG"])
    print(f"Exercise 1: filename={args.filename}, count={args.count}, "
          f"prefix='{args.prefix}'")
    assert args.filename == "data.txt"
    assert args.count == 5
    assert args.prefix == "LOG"

exercise1()
print("---")


# ============================================================
# Exercise 2: Mutually exclusive group --json vs --csv
# ============================================================

def exercise2() -> None:
    """Simulate choosing one output format among mutually exclusive options."""
    parser = argparse.ArgumentParser(description="Export data.")
    fmt_group = parser.add_mutually_exclusive_group(required=True)
    fmt_group.add_argument("--json", action="store_true",
                           help="Export as JSON")
    fmt_group.add_argument("--csv", action="store_true",
                           help="Export as CSV")
    # Simulate --json
    args_json = parser.parse_args(["--json"])
    print(f"Exercise 2: json={args_json.json}, csv={args_json.csv}")
    assert args_json.json is True and args_json.csv is False

    # Simulate --csv (re-run in a fresh parser to avoid conflict)
    args_csv = argparse.ArgumentParser().add_argument_group  # dummy placeholder
    parser2 = argparse.ArgumentParser(description="Export data.")
    g2 = parser2.add_mutually_exclusive_group(required=True)
    g2.add_argument("--json", action="store_true")
    g2.add_argument("--csv", action="store_true")
    args_csv = parser2.parse_args(["--csv"])
    print(f"           json={args_csv.json}, csv={args_csv.csv}")
    assert args_csv.csv is True and args_csv.json is False

    # Mutually exclusive means passing both should error
    parser3 = argparse.ArgumentParser(description="Export data.")
    g3 = parser3.add_mutually_exclusive_group(required=True)
    g3.add_argument("--json", action="store_true")
    g3.add_argument("--csv", action="store_true")
    try:
        parser3.parse_args(["--json", "--csv"])
    except SystemExit:
        print("           Correctly rejected --json --csv together")
    else:
        raise AssertionError("Should have rejected both flags together")

exercise2()
print("---")


# ============================================================
# Exercise 3: Subcommands (list, add, delete) for a todo mgr
# ============================================================

# In-memory todo store so the exercise exercises subcommand dispatch
TODO_STORE: list[str] = []

def _cmd_list(args: argparse.Namespace) -> None:
    """List all todo items."""
    if not TODO_STORE:
        print("           (empty)")
    for i, item in enumerate(TODO_STORE, 1):
        done = "✓" if args.show_done else " "
        print(f"           [{done}] {i}. {item}")

def _cmd_add(args: argparse.Namespace) -> None:
    """Add a new todo item."""
    TODO_STORE.append(args.text)
    print(f"           Added: '{args.text}'")

def _cmd_delete(args: argparse.Namespace) -> None:
    """Delete a todo item by index."""
    idx = args.index - 1  # user-facing is 1-indexed
    if 0 <= idx < len(TODO_STORE):
        removed = TODO_STORE.pop(idx)
        print(f"           Deleted: '{removed}'")
    else:
        print(f"           Invalid index: {args.index}")

def exercise3() -> None:
    """Simulate subcommands: add → add → list → delete."""
    parser = argparse.ArgumentParser(description="Todo manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List all items")
    p_list.add_argument("--show-done", action="store_true",
                        help="Show completed items")
    p_list.set_defaults(func=_cmd_list)

    p_add = sub.add_parser("add", help="Add a new item")
    p_add.add_argument("text", help="Todo text")
    p_add.set_defaults(func=_cmd_add)

    p_del = sub.add_parser("delete", help="Delete an item")
    p_del.add_argument("index", type=int, help="Item number to delete")
    p_del.set_defaults(func=_cmd_delete)

    print("Exercise 3:")
    # Dispatch a sequence of subcommands
    for cmd_args in [
        ["add", "Comprar pan"],
        ["add", "Terminar informe de Carlos"],
        ["list"],
        ["delete", "1"],
        ["list"],
    ]:
        ns = parser.parse_args(cmd_args)
        ns.func(ns)

    assert TODO_STORE == ["Terminar informe de Carlos"]
    TODO_STORE.clear()

exercise3()
print("---")


# ============================================================
# Exercise 4: Custom validation (port range 1-65535, email
#            format check)
# ============================================================

def port_range(value: str) -> int:
    """Argparse type: validate port is in 1-65535."""
    port = int(value)
    if not (1 <= port <= 65535):
        raise argparse.ArgumentTypeError(
            f"Port {port} is out of range (1-65535)")
    return port

def email_format(value: str) -> str:
    """Argparse type: validate basic email format."""
    # Simple regex: user@domain.tld
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, value):
        raise argparse.ArgumentTypeError(
            f"'{value}' is not a valid email address")
    return value

def exercise4() -> None:
    """Simulate validation with good and bad inputs."""
    parser = argparse.ArgumentParser(description="Server config")
    parser.add_argument("--port", type=port_range, default=8080,
                        help="Listen port (1-65535)")
    parser.add_argument("--email", type=email_format,
                        help="Admin email")

    print("Exercise 4:")
    # Happy path
    args_good = parser.parse_args(["--port", "443", "--email",
                                    "carlos@empresa.es"])
    print(f"           port={args_good.port}, email={args_good.email}")
    assert args_good.port == 443

    # Invalid port
    try:
        parser.parse_args(["--port", "99999"])
    except SystemExit:
        print("           Correctly rejected port 99999 (out of range)")

    # Invalid email
    try:
        parser.parse_args(["--email", "not-an-email"])
    except SystemExit:
        print("           Correctly rejected invalid email format")

exercise4()
print("---")


# ============================================================
# BONUS: Rewrite exercise 3 using typer
# ============================================================

def bonus() -> None:
    """Same todo manager as Exercise 3, but built with Typer."""
    try:
        import typer
    except ImportError:
        print("BONUS:    ⚠ typer not installed — skipping (pip install typer)")
        return

    typer_todo: list[str] = []       # in-memory store for the Typer version

    app = typer.Typer(help="Todo manager (Typer edition)")

    @app.command(name="list")
    def list_items(show_done: bool = typer.Option(
            False, "--show-done", help="Show completed items")):
        """List all todo items."""
        if not typer_todo:
            typer.echo("    (empty)")
            return
        for i, item in enumerate(typer_todo, 1):
            done = "✓" if show_done else " "
            typer.echo(f"    [{done}] {i}. {item}")

    @app.command()
    def add(text: str = typer.Argument(..., help="Todo text")):
        """Add a new todo item."""
        typer_todo.append(text)
        typer.echo(f"    Added: '{text}'")

    @app.command()
    def delete(index: int = typer.Argument(..., help="Item number to delete")):
        """Delete a todo item by index."""
        idx = index - 1
        if 0 <= idx < len(typer_todo):
            removed = typer_todo.pop(idx)
            typer.echo(f"    Deleted: '{removed}'")
        else:
            typer.echo(f"    Invalid index: {index}")

    print("BONUS:")
    # Simulate the same sequence by calling the CLI runner directly
    # Typer can be invoked programmatically via CliRunner
    from typer.testing import CliRunner
    runner = CliRunner()

    for cmd, expect_ok in [
        (["add", "Comprar pan"], True),
        (["add", "Terminar informe de Carlos"], True),
        (["list"], True),
        (["delete", "1"], True),
        (["list"], True),
    ]:
        result = runner.invoke(app, cmd)
        if expect_ok:
            assert result.exit_code == 0, f"Command {cmd} failed: {result.stdout}"
        # runner.invoke output is captured, so we print it
        for line in result.stdout.strip().splitlines():
            print(f"           {line}")

    assert typer_todo == ["Terminar informe de Carlos"]

bonus()

print("---")
print("✅ All Group 02 exercises passed!")
