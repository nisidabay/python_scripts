#!/usr/bin/env python3
# argparse_06: Subcommands with subparsers + dispatch pattern — a database migration tool
import argparse


def cmd_init(args):
    """Create a new migrations directory."""
    print(f"Initializing migrations in: {args.dir}")


def cmd_create(args):
    """Scaffold a new migration file."""
    print(f"Creating migration '{args.name}' (auto-timestamped)")


def cmd_apply(args):
    """Run pending migrations against target DB."""
    target = "all pending" if args.all else f"up to {args.limit}"
    print(f"Applying {target} migrations on {args.dsn}…")


def cmd_rollback(args):
    """Roll back the last N migrations."""
    print(f"Rolling back {args.steps} migration(s) on {args.dsn}…")


parser = argparse.ArgumentParser(description="Database migration tool — manage schema versions.")
sub = parser.add_subparsers(dest="command", required=True, help="Sub-command to run")

# init
p_init = sub.add_parser("init", help="Create a migrations directory")
p_init.add_argument("--dir", default="./migrations", help="Target directory")
p_init.set_defaults(func=cmd_init)

# create
p_create = sub.add_parser("create", help="Scaffold a new migration")
p_create.add_argument("name", help="Descriptive migration name (e.g. 'add_users_table')")
p_create.set_defaults(func=cmd_create)

# apply
p_apply = sub.add_parser("apply", help="Run pending migrations")
p_apply.add_argument("dsn", help="Database connection string")
p_apply.add_argument("--all", action="store_true", help="Apply all pending (default)")
p_apply.add_argument("--limit", type=int, metavar="N", help="Apply at most N migrations")
p_apply.set_defaults(func=cmd_apply)

# rollback
p_rollback = sub.add_parser("rollback", help="Roll back migrations")
p_rollback.add_argument("dsn", help="Database connection string")
p_rollback.add_argument("--steps", type=int, default=1, help="Number of migrations to undo")
p_rollback.set_defaults(func=cmd_rollback)

args = parser.parse_args()
args.func(args)  # dispatch to the appropriate handler


if __name__ == "__main__":
    pass
