# Foundations — Python idioms, typing, pathlib, dataclasses, errors, stdlib gems, env vars

## Quick Start
```bash
python 01_idioms.py
python 02_pathlib.py
python 03_typing.py
python 04_dataclasses.py
python 05_errors.py
python 06_stdlib_gems.py
python 07_env_vars.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `01_idioms.py` | Comprehensions, unpacking, f-strings, walrus | `{n for n in names}`, `first, *rest = items`, `f"{name:>8}"`, `if (n := len(x)) > 3:` |
| `02_pathlib.py` | Modern file paths with `pathlib` | `Path.home() / "dir"`, `.read_text()`, `.glob("**/*.log")`, `.iterdir()` |
| `03_typing.py` | Type hints for static analysis | `Optional[X]`, `Union[int, str]`, `Literal["debug","info"]`, `Protocol`, `TypeAlias` |
| `04_dataclasses.py` | Boilerplate-free data classes | `@dataclass(order=True, frozen=True)`, `field(default_factory=list)`, `asdict()`, `replace()` |
| `05_errors.py` | Custom exceptions, exception chaining | `raise CustomError(...) from e`, `try/else/finally`, custom `Exception` subclasses |
| `06_stdlib_gems.py` | Power tools from the standard library | `Counter`, `itertools.chain/groupby/product`, `@lru_cache`, `statistics.mean/stdev` |
| `07_env_vars.py` | Config from env vars, CLI+env, .env files | `os.environ.get("KEY", default)`, `argparse` env fallback, manual `.env` parser |

## Common Patterns
```python
# Comprehensions and unpacking
unique = {n for n in names}                            # set comprehension
mapped = {k: len(k) for k in unique}                   # dict comprehension
first, *rest = items                                    # star unpacking
merged = {**d1, **d2}                                  # dict merge

# Pathlib — never os.path again
from pathlib import Path
home = Path.home()
cfg = home / ".config" / "myapp" / "settings.toml"
text = cfg.read_text()                                 # one-liner read

# Dataclasses — write zero __init__
from dataclasses import dataclass, field, asdict, replace
@dataclass(order=True, frozen=True)
class Point:
    x: float
    y: float
    label: str = "origin"

# Custom exceptions with chaining
class AppError(Exception):
    def __init__(self, msg, path=""):
        super().__init__(msg)
        self.path = path
raise AppError("missing config", str(cfg)) from FileNotFoundError

# Stdlib gems
from collections import Counter
tally = Counter(votes)
tally.most_common(3)                                   # top N

from functools import lru_cache
@lru_cache(maxsize=128)
def expensive(n): ...

# Env vars with fallback
db_host = os.environ.get("DB_HOST", "localhost")
```

## Now Build Your Own
Write a script `profile_report.py` that:
1. Uses `pathlib` to find all `.json` files under `~/.config/` recursively.
2. Loads each JSON file (handle `FileNotFoundError`/`JSONDecodeError` with custom exceptions).
3. Uses `Counter` to tally how many files were in each subdirectory.
4. Prints a formatted report using f-strings with alignment.
5. Accepts a `--verbose` flag via `argparse` (default from `VERBOSE` env var).
6. Uses a `@dataclass` to represent each file's metadata (path, size, key_count).
