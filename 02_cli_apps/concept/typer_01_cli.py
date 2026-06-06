#!/usr/bin/env python3
# typer_01: Same migration tool as argparse_06 but with Typer — modern, type-hint-driven CLI
import typer
from typing import Optional

app = typer.Typer(help="Database migration tool — manage schema versions.")


def version_callback(value: bool):
    """Print version and exit."""
    if value:
        typer.echo("migrate-tool v2.1.0")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True,
        help="Show version and exit",
    ),
):
    """Migration tool entrypoint — use subcommands below."""
    pass


@app.command()
def init(directory: str = typer.Option("./migrations", "--dir",
                                         help="Target directory for migrations")):
    """Create a new migrations directory."""
    typer.echo(f"Initializing migrations in: {directory}")


@app.command()
def create(name: str = typer.Argument(..., help="Descriptive migration name (e.g. 'add_users_table')")):
    """Scaffold a new migration file."""
    typer.echo(f"Creating migration '{name}' (auto-timestamped)")


@app.command()
def apply(
    dsn: str = typer.Argument(..., help="Database connection string"),
    all_: bool = typer.Option(True, "--all/--no-all", help="Apply all pending migrations"),
    limit: Optional[int] = typer.Option(None, "--limit", help="Apply at most N migrations"),
):
    """Run pending migrations against target DB."""
    target = "all pending" if all_ else f"up to {limit}"
    typer.echo(f"Applying {target} migrations on {dsn}…")


@app.command()
def rollback(
    dsn: str = typer.Argument(..., help="Database connection string"),
    steps: int = typer.Option(1, "--steps", help="Number of migrations to undo"),
):
    """Roll back the last N migrations."""
    typer.echo(f"Rolling back {steps} migration(s) on {dsn}…")


if __name__ == "__main__":
    app()
