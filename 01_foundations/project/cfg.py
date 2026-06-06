#!/usr/bin/env python3
"""Config file CLI: reads YAML/JSON/TOML-like config, merges with env vars, prints resolved config.

Uses: pathlib, argparse, dataclass, typing — stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, Optional


# ---------------------------------------------------------------------------
# Tiny "TOML-like" parser (no third-party toml module)
# ---------------------------------------------------------------------------
def parse_toml_like(text: str) -> Dict[str, Any]:
    """Parse a simple TOML-like config (sections, key=value, strings, bools, ints, lists)."""
    result: Dict[str, Any] = {}
    current_section: Optional[str] = None
    current_map: Dict[str, Any] = result

    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        # Section header  [section]
        m = re.match(r"^\[(.+)]$", line)
        if m:
            section = m.group(1).strip()
            if section not in result:
                result[section] = {}
            current_section = section
            current_map = result[section]
            continue

        # key = value
        m = re.match(r'^([a-zA-Z_]\w*)\s*=\s*(.+)$', line)
        if not m:
            print(f"Warning: skipping line {lineno}: {raw!r}", file=sys.stderr)
            continue

        key = m.group(1)
        raw_val = m.group(2).strip()

        # Try to parse the value
        val: Any
        if raw_val.lower() == "true":
            val = True
        elif raw_val.lower() == "false":
            val = False
        elif raw_val.lower() in ("null", "none"):
            val = None
        elif (raw_val.startswith('"') and raw_val.endswith('"')) or \
             (raw_val.startswith("'") and raw_val.endswith("'")):
            val = raw_val[1:-1]
        elif re.match(r"^\d+\.\d+$", raw_val):
            val = float(raw_val)
        elif re.match(r"^[-+]?\d+$", raw_val):
            val = int(raw_val)
        elif raw_val.startswith("[") and raw_val.endswith("]"):
            # Simple list parser
            items = raw_val[1:-1].split(",")
            val = [_parse_scalar(it.strip().strip('"').strip("'")) for it in items if it.strip()]
        else:
            val = raw_val  # keep as string

        current_map[key] = val

    return result


def _parse_scalar(s: str) -> Any:
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    if re.match(r"^[-+]?\d+$", s):
        return int(s)
    if re.match(r"^\d+\.\d+$", s):
        return float(s)
    return s


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass
class AppConfig:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    database_url: str = ""
    extras: Dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------
def load_json(path: Path) -> Dict[str, Any]:
    """Load config from a JSON file."""
    with open(path) as f:
        return json.load(f)


def load_toml(path: Path) -> Dict[str, Any]:
    """Load config from a TOML-like file."""
    with open(path) as f:
        return parse_toml_like(f.read())


def merge_env(config: AppConfig, prefix: str = "APP_") -> AppConfig:
    """Merge environment variables (APP_HOST, APP_PORT, ...) into config."""
    for key, value in os.environ.items():
        if not key.startswith(prefix):
            continue
        field = key[len(prefix):].lower()
        if field in ("host", "database_url"):
            setattr(config, field, value)
        elif field == "port":
            try:
                setattr(config, field, int(value))
            except ValueError:
                pass
        elif field == "debug":
            setattr(config, field, value.lower() in ("1", "true", "yes"))
        else:
            config.extras[field] = value
    return config


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Load config (JSON or TOML), merge env vars, print resolved config."
    )
    p.add_argument("config_file", type=Path, help="Path to config file (JSON or .toml-like)")
    p.add_argument("--prefix", default="APP_", help="Env var prefix (default: APP_)")
    p.add_argument("--json-output", action="store_true", help="Output as JSON instead of Python dict")
    return p


def main() -> None:
    args = build_arg_parser().parse_args()

    config_path: Path = args.config_file
    if not config_path.exists():
        print(f"Error: file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    suffix = config_path.suffix.lower()
    if suffix == ".json":
        raw = load_json(config_path)
    else:
        raw = load_toml(config_path)

    # Build AppConfig from raw dict
    cfg = AppConfig(
        host=raw.get("host", "localhost"),
        port=int(raw.get("port", 8080)),
        debug=bool(raw.get("debug", False)),
        database_url=raw.get("database_url", ""),
        extras={k: v for k, v in raw.items() if k not in ("host", "port", "debug", "database_url")},
    )

    cfg = merge_env(cfg, prefix=args.prefix)

    result = asdict(cfg)

    if args.json_output:
        print(json.dumps(result, indent=2))
    else:
        for key, val in result.items():
            print(f"{key}: {val!r}")


if __name__ == "__main__":
    main()
