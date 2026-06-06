# Context Managers — writable file, suppress, timer, tempdir

## Quick Start
```bash
python 07_writable_file.py
python 07_suppress.py
python 07_timer.py
python 07_tempdir.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `07_writable_file.py` | Class-based context manager (`__enter__`/`__exit__`) | `__enter__` opens file returns `TextIO`, `__exit__` closes it |
| `07_suppress.py` | `contextlib.suppress` + `@contextmanager` decorator | `with suppress(FileNotFoundError):`, `@contextmanager` with `yield` |
| `07_timer.py` | Measure execution time with class-based and decorator-based CM | `time.perf_counter()` in `__enter__`/`__exit__`, `@contextmanager def timer()` |
| `07_tempdir.py` | `tempfile.TemporaryDirectory` + manual + conditional cleanup | Built-in auto-cleanup, `tempfile.mkdtemp()`, `shutil.rmtree()`, optional persistent dir |

## Common Patterns
```python
from contextlib import contextmanager, suppress
import time, tempfile, shutil
from pathlib import Path

# --- Class-based context manager ---
class WritableFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.file_obj = open(self.file_path, mode="w")
        return self.file_obj                   # becomes the 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj:
            self.file_obj.close()
        return False  # don't suppress exceptions

# --- @contextmanager decorator (generator-based) ---
@contextmanager
def timer(label="Block"):
    start = time.perf_counter()
    try:
        yield                                   # hand control to with-block
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] took {elapsed:.4f}s")

# --- contextlib.suppress (ignore specific exceptions) ---
with suppress(FileNotFoundError):
    Path("/nonexistent").read_text()            # silently skip

with suppress(ZeroDivisionError, TypeError):
    result = 1 / 0                              # also suppressed

# --- tempfile.TemporaryDirectory (built-in) ---
with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    (tmp_path / "data.txt").write_text("temp data")
# Directory auto-deleted after block

# --- Manual temp dir with cleanup ---
class ManagedTempDir:
    def __init__(self, prefix="temp_"):
        self.prefix = prefix

    def __enter__(self):
        self.path = Path(tempfile.mkdtemp(prefix=self.prefix))
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path.exists():
            shutil.rmtree(self.path)
        return False

# --- Conditional cleanup (persistent if dir given) ---
class OptionalTempDir:
    def __init__(self, directory=None):
        self.given_dir = directory
        self._cleanup = False

    def __enter__(self):
        if self.given_dir:
            path = Path(self.given_dir)
            path.mkdir(parents=True, exist_ok=True)
        else:
            path = Path(tempfile.mkdtemp())
            self._cleanup = True
        self.path = path
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._cleanup and self.path.exists():
            shutil.rmtree(self.path)
        return False

# --- Restore state with context manager ---
@contextmanager
def temporary_attribute(obj, name, value):
    original = getattr(obj, name, None)
    setattr(obj, name, value)
    try:
        yield obj
    finally:
        setattr(obj, name, original)            # always restore
```

## Now Build Your Own
Write `context_manager_utils.py` with:
1. A class-based `DatabaseConnection` context manager that simulates `connect()` on `__enter__` and `close()` on `__exit__` (print instead of real DB). Return a `cursor` object from `__enter__`.
2. A `@contextmanager`-based `working_directory(path)` that `chdir`s to `path` on enter and restores the original directory on exit (use `os.getcwd()` / `os.chdir()`).
3. A `LoggedSuppress` context manager class that suppresses specified exceptions but prints a log message for each suppressed exception (use `__exit__` returning `True` for suppressed types, `False` otherwise).
4. A `TimedBlock` using `@contextmanager` that takes a `name` parameter and prints `[NAME] started...` on enter and `[NAME] finished in X.XXXs` on exit.
5. Use `suppress` to safely delete a file that might not exist, then write a new one in its place.
