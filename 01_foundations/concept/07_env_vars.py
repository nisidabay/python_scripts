#!/usr/bin/env python3
# Configuration: environment variables, CLI args with env fallback, .env files.

import os
import argparse
from pathlib import Path

# os.environ: read env vars directly — KeyError if missing, .get() for safe access
db_host = os.environ.get("DB_HOST", "localhost")  # default if not set
db_port = int(os.environ.get("DB_PORT", "5432"))  # env vars are always strings
print(f"DB target: {db_host}:{db_port}")

# argparse with env-var fallback: CLI wins, env is backup
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Database migrator")
    p.add_argument("--host", default=os.environ.get("DB_HOST", "localhost"),
                   help="Database host (env: DB_HOST)")
    p.add_argument("--port", type=int,
                   default=int(os.environ.get("DB_PORT", "5432")),
                   help="Database port (env: DB_PORT)")
    p.add_argument("--user", default=os.environ.get("DB_USER", "admin"),
                   help="Database user (env: DB_USER)")
    p.add_argument("--dry-run", action="store_true",
                   default=os.environ.get("DRY_RUN", "0") == "1",
                   help="Preview only (env: DRY_RUN=1)")
    return p.parse_args([])  # empty list = use defaults (no CLI args passed)

args = parse_args()
print(f"Resolved config: {args.host}:{args.port} as {args.user}, dry_run={args.dry_run}")

# .env pattern: load key=value pairs into os.environ (manual for demo)
def load_dotenv(path: Path) -> dict[str, str]:
    """Parse a .env file into a dict — no third-party dependency."""
    vars_dict: dict[str, str] = {}
    if not path.exists():
        return vars_dict
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):  # skip comments and blanks
            continue
        if "=" in line:
            key, _, value = line.partition("=")  # partition: split on first =
            vars_dict[key.strip()] = value.strip().strip("\"'")
    return vars_dict

# Write a demo .env and load it
env_path = Path("/tmp/demo.env")
env_path.write_text("""
# Database settings for Carlos's project
DB_HOST=db.example.com
DB_PORT=5433
DB_USER=carlos_admin
DRY_RUN=1
""")
env_vars = load_dotenv(env_path)
print(f".env loaded: {env_vars}")

# Apply .env values only if not already set in environment
for key, value in env_vars.items():
    os.environ.setdefault(key, value)  # setdefault: env wins over .env

# Path.home() for config file discovery
config_dir = Path.home() / ".config" / "myapp"
config_dir.mkdir(parents=True, exist_ok=True)
(config_dir / "settings.json").write_text('{"theme": "dark"}')
print(f"Config stored at: {config_dir}")

# Cleanup
env_path.unlink(missing_ok=True)
(config_dir / "settings.json").unlink()
config_dir.rmdir()

if __name__ == "__main__":
    assert args.host == "localhost", "Default should be localhost"
    print("env vars checks passed")
