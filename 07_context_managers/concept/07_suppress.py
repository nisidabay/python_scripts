#!/usr/bin/env python3
# Context manager: contextlib.suppress + @contextmanager decorator for exception handling
from contextlib import suppress, contextmanager
from pathlib import Path


# --- contextlib.suppress: silently ignore specified exceptions ---
# Useful when you expect and want to ignore specific errors (e.g., file not found)
with suppress(FileNotFoundError):
    Path("/tmp/does_not_exist_xyz").read_text()  # silently skipped
    print("This won't print because FileNotFoundError is suppressed above")

# suppress can take multiple exception types
with suppress(ZeroDivisionError, TypeError):
    result = 1 / 0  # ZeroDivisionError suppressed
    print("This also won't print")


# --- @contextmanager decorator: turn a generator into a context manager ---
# yield splits the function: before yield = __enter__, after yield = __exit__
@contextmanager
def temporary_attribute(obj, name, value):
    """Temporarily set an attribute, restore original on exit."""
    original = getattr(obj, name, None)      # __enter__: save state
    setattr(obj, name, value)                 # __enter__: apply change
    print(f"  [ENTER] {name} set to {value!r}")
    try:
        yield obj                             # hand control to the with-block
    finally:
        setattr(obj, name, original)          # __exit__: always restore
        print(f"  [EXIT]  {name} restored to {original!r}")


# Demonstration with a simple class
class Config:
    debug = False


if __name__ == "__main__":
    cfg = Config()
    print(f"Before: cfg.debug = {cfg.debug}")

    with temporary_attribute(cfg, "debug", True) as c:
        print(f"Inside: c.debug = {c.debug}")

    print(f"After:  cfg.debug = {cfg.debug}")
