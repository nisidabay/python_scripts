# Logging — Custom loggers, multiple loggers, file handler configuration

## Quick Start
```bash
# Custom logger with colored console output + file handler
python 09_custom_logger.py

# Two independent loggers (one console, one file) with different levels
python 09_different_loggers.py

# Basic file-based logger setup
python 09_filehandler_logger.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `09_custom_logger.py` | Dataclass-based configurable logger with file + optional console handlers, colored formatter | `@dataclass` logger config, `CustomFormatter` with ANSI color levels, `__post_init__` wiring |
| `09_different_loggers.py` | Multiple named loggers with independent levels and destinations | `getLogger("name")` isolation, `StreamHandler` vs `FileHandler`, per-logger formatters |
| `09_filehandler_logger.py` | Minimal `basicConfig` setup logging to a file | One-shot `logging.basicConfig(filename=…)` with format string |

## Common Patterns
```python
import logging

# Custom logger class pattern
class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG:    "\x1b[38;21m%(asctime)s - %(name)s - %(levelname)s - %(message)s\x1b[0m",
        logging.INFO:     "\x1b[32;21m%(asctime)s - %(name)s - %(levelname)s - %(message)s\x1b[0m",
        logging.WARNING:  "\x1b[33;21m%(asctime)s - %(name)s - %(levelname)s - %(message)s\x1b[0m",
        logging.ERROR:    "\x1b[31;21m%(asctime)s - %(name)s - %(levelname)s - %(message)s\x1b[0m",
        logging.CRITICAL: "\x1b[31;1m%(asctime)s - %(name)s - %(levelname)s - %(message)s\x1b[0m",
    }
    def format(self, record):
        return logging.Formatter(self.FORMATS.get(record.levelno)).format(record)

# Multiple loggers with independent configuration
logger1 = logging.getLogger("logger1")
logger1.setLevel(logging.DEBUG)
logger1.addHandler(logging.StreamHandler())   # console

logger2 = logging.getLogger("logger2")
logger2.setLevel(logging.WARNING)
logger2.addHandler(logging.FileHandler("app.log"))  # file

# Quick file-only setup
logging.basicConfig(
    filename="app.log", level=logging.INFO,
    format="%(levelname)s %(asctime)s - ln: %(lineno)s - %(message)s",
    filemode="a"
)
logger = logging.getLogger("myapp")
```

## Now Build Your Own
**Challenge:** Build a `tiered_logger.py` that writes DEBUG-level messages to a `debug.log` file and INFO+ messages to `console`. Create both handlers programmatically (no `basicConfig`), use different formatters for each handler, and include timestamps. Log 3 messages at each level to verify the routing works correctly.
