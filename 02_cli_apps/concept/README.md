# CLI Apps — argparse crescendo series + Typer capstone

## Quick Start
```bash
python argparse_01_basic_flags.py --verbose --dry-run
python argparse_02_positional.py input.mp4 output.avi
python argparse_03_types.py --replicas 3 --cpu 1.0 --output csv host1 host2
python argparse_04_defaults.py --lines 100 --tail
python argparse_05_mutual_exclusion.py --email carlos@example.com "Deploy complete"
python argparse_06_subcommands.py apply postgresql://localhost/db --all
python argparse_07_validation.py --port 8080 --config /etc/hosts
python argparse_08_help_formatting.py --version 2.3.0 --help
python typer_01_cli.py apply postgresql://localhost/db --all
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `argparse_01_basic_flags.py` | Boolean flags with `store_true` | `add_argument("--verbose", action="store_true")` |
| `argparse_02_positional.py` | Required positional arguments + metavar | `add_argument("input_file", metavar="INPUT")` |
| `argparse_03_types.py` | `type=` casting, `choices=`, `nargs` | `type=int`, `choices=["json","csv"]`, `nargs="+"` |
| `argparse_04_defaults.py` | `nargs='?'` with `const`, `set_defaults()` | `nargs="?", const=10`, `parser.set_defaults(max_mb=500)` |
| `argparse_05_mutual_exclusion.py` | Mutually exclusive group (one required) | `add_mutually_exclusive_group(required=True)` |
| `argparse_06_subcommands.py` | Subparsers + function dispatch | `subparsers`, `set_defaults(func=handler)`, `args.func(args)` |
| `argparse_07_validation.py` | Custom `type=` function, custom `Action` class | `def port_number(value)`, `class EnvVarAction(argparse.Action)` |
| `argparse_08_help_formatting.py` | Formatter class, epilog, `%(default)s` in help | `RawDescriptionHelpFormatter`, `epilog=EXAMPLES`, `"default: %(default)s"` |
| `typer_01_cli.py` | Modern CLI with type-hint-driven interface | `@app.command()`, `typer.Option(...)`, `typer.Argument(...)`, `@app.callback()` |

## Common Patterns
```python
import argparse

# Basic boolean flags
parser = argparse.ArgumentParser(description="Tool description")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
parser.add_argument("--dry-run", action="store_true")

# Positional + types
parser.add_argument("input", metavar="FILE", help="Source file")
parser.add_argument("--count", type=int, default=1)
parser.add_argument("--mode", choices=["fast", "full"], default="fast")
parser.add_argument("hosts", nargs="+", metavar="HOST")

# nargs='?' with const
parser.add_argument("--tail", nargs="?", const=10, type=int)

# Mutually exclusive
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--email")
group.add_argument("--sms")

# Subcommands with dispatch
sub = parser.add_subparsers(dest="command", required=True)
p_apply = sub.add_parser("apply")
p_apply.add_argument("dsn")
p_apply.set_defaults(func=cmd_apply)

args = parser.parse_args()
args.func(args)  # dispatch

# Custom type validation
def valid_port(value):
    p = int(value)
    if not 1 <= p <= 65535:
        raise argparse.ArgumentTypeError(f"port {p} out of range")
    return p

# Typer (modern alternative)
import typer
app = typer.Typer()

@app.command()
def apply(dsn: str, all_: bool = typer.Option(True, "--all/--no-all")):
    typer.echo(f"Applying to {dsn}")

if __name__ == "__main__":
    app()
```

## Now Build Your Own
Build a CLI tool `task_manager.py` that:
1. Has subcommands: `add`, `list`, `done`, and `report`.
2. `add` takes a required positional `TASK_DESCRIPTION` and optional `--priority` (choices: low/medium/high, default: medium).
3. `list` takes `--status` with choices pending/done/all (default: pending) and `--limit N` (int).
4. `done` takes one or more task IDs (`nargs="+"`, type=int).
5. `report` takes `--format` (json/csv/table, default: table) and `--output FILE`.
6. Include a `--version` flag that prints version and exits.
7. Use `RawDescriptionHelpFormatter` with an epilog showing examples.
8. Rewrite the whole thing with Typer as `task_manager_typer.py`.
