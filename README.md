# Python Practice — From Scripts to Systems

A progressive, code-first curriculum for deepening Python through real CLI tools,
data pipelines, and desktop apps. No notebooks, no frameworks — just the standard
library, pandas/numpy, and real problems.

## Who This Is For

- You already write Python scripts and want to level up
- You want to understand decorators, generators, asyncio, and OOP deeply
- You want to build CLI tools, TUI dashboards, and data pipelines
- You learn by reading real code, then writing your own

## Two Paths In

### Path A: Quick Tour (~30 min)

Jump into any group that interests you and run `python3` on the concept files:

```bash
cd 02_cli_apps/concept
cat README.md              # see the map
python3 argparse_01_basic_flags.py --help
python3 argparse_06_subcommands.py add "learn python" --priority high
```

### Path B: Systematic (~several weeks)

Work through the 15 numbered groups in order. Each group has:

- **concept/README.md** — quick-start table + learning path
- **concept/*.py** — one concept per file, code-first, runnable standalone
- **exercises.py** — 4 solved practice problems + BONUS challenge
- **project/** — a real CLI tool using those concepts
- **"Now Build Your Own"** prompt at the bottom of every README

## The Groups

| # | Group | What You'll Build |
|---|-------|-------------------|
| 01 | `foundations` | Python idioms: comprehensions, pathlib, dataclasses, typing, errors, env vars |
| 02 | `cli_apps` | argparse crescendo series (01–08) + typer capstone |
| 03 | `functions` | Decorators, closures, partial, memoization, lambdas |
| 04 | `classes_oop` | @classmethod, @property, descriptors, composition, singleton |
| 05 | `iterators_generators` | __iter__/__next__, yield, generator expressions, lazy evaluation |
| 06 | `collections` | namedtuple, defaultdict, Counter, ChainMap, deque, linked lists |
| 07 | `context_managers` | with, __enter__/__exit__, @contextmanager, ExitStack |
| 08 | `filesystem` | pathlib, os, shutil, file stats, tree, atomic writes |
| 09 | `logging` | Logger hierarchy, handlers, formatters, rotating files |
| 10 | `data` | pandas (Series, DataFrame, groupby, pivot) + numpy (arrays, ufuncs, broadcasting) |
| 11 | `concurrency` | Threads, ThreadPoolExecutor, asyncio, multiprocessing |
| 12 | `networking` | Sockets, requests, smtplib, BeautifulSoup, URL parsing |
| 13 | `system` | subprocess, signals, psutil-style monitoring, encryption |
| 14 | `tui` | Rich (tables, progress, panels, live) + Textual (apps, widgets, events) |
| 15 | `desktop` | Tkinter fundamentals, MVC pattern, real GUI app |

Start here:

```bash
cd 01_foundations/concept
cat README.md
python3 01_idioms.py
```

Then keep going: `02_cli_apps` → `03_functions` → … → `15_desktop`.

## Prerequisites

```bash
# Core (stdlib-only for groups 01-09, 11-13, 15)
python3 --version   # 3.10+

# Group 10 (data)
pip install pandas numpy

# Group 14 (tui)
pip install rich textual
```

## The raw/ Directory

Scripts that didn't fit the curriculum live in `raw/` — Bender voice assistant,
Pillow image tools, coding exercises, streamlit experiments, and general utilities.
They're preserved for reference, not deleted.

## Additional Resources

See [REFERENCES.md](REFERENCES.md) for books, courses, and documentation.
