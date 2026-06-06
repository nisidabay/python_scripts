#!/usr/bin/env python3
# Error handling: catch what you can fix, let the rest surface.

import json
from pathlib import Path
from typing import Any

# Custom exception — subclass Exception, add context
class ConfigError(Exception):
    """Configuration is missing or malformed."""
    def __init__(self, message: str, path: str = ""):
        super().__init__(message)
        self.path = path  # extra context for debugging

class ValidationError(ConfigError):
    """Config values don't pass business rules."""
    pass

def load_config(path: Path) -> dict[str, Any]:
    """Load JSON config with layered error handling."""
    try:
        raw = path.read_text()  # FileNotFoundError if missing
    except FileNotFoundError as e:
        # raise from: chain exceptions, preserving original traceback
        raise ConfigError(f"Config file not found: {path}", str(path)) from e

    try:
        data = json.loads(raw)  # json.JSONDecodeError if malformed
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in {path}", str(path)) from e
    else:
        # else runs ONLY if try succeeded — separates happy path from error path
        print(f"Parsed config with {len(data)} keys")
        return data
    finally:
        # finally ALWAYS runs — cleanup even after raise/return
        print(f"Finished attempting to load {path.name}")

def validate_age(name: str, age: int) -> None:
    """Business rule: ages must be positive."""
    assert age > 0, f"Age for {name} must be positive, got {age}"  # dev-only check
    if age > 150:
        raise ValidationError(f"Age for {name} is implausible: {age}")

def run_demo() -> None:
    # Happy path
    try:
        data = {"Carlos": 34}
        for name, age in data.items():
            validate_age(name, age)
        print(f"All {len(data)} entries validated")
    except ValidationError as e:
        print(f"Validation failed: {e}")
    except ConfigError:
        print("Config issue — can't continue")

    # Deliberate failure demo
    try:
        validate_age("Zorg", -5)
    except AssertionError as e:
        print(f"Caught assertion: {e}")  # assert fires AssertionError

if __name__ == "__main__":
    run_demo()

    # Verify custom exception chaining
    try:
        load_config(Path("/nonexistent/config.json"))
    except ConfigError as e:
        assert e.__cause__ is not None, "raise from should preserve cause"
        assert isinstance(e.__cause__, FileNotFoundError)
    print("error handling checks passed")
