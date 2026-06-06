# Filesystem Operations — Recursive stats, auto-organize, directory tree, smart file updates

## Quick Start
```bash
# File statistics by extension (run on current directory)
python 08_files_stats.py

# Organize files into subfolders by type
python 08_organize_files.py [directory_path]

# Print directory tree (modify startpath variable first)
python 08_tree.py

# Replace old file only if contents changed
python 08_update_file.py <old_file> <new_file>
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `08_files_stats.py` | Recursive file/directory traversal with `os.walk`, extension grouping, tabular reporting | Class-based stats collector with `setdefault` aggregation |
| `08_organize_files.py` | File type detection via extension, folder creation, `shutil.move` | Dict-based type mapping, guard clauses for existing dirs |
| `08_tree.py` | Visual tree rendering with `os.walk`, depth-based indentation | Recursive tree using `os.sep` count for indent level |
| `08_update_file.py` | Atomic file replacement — only overwrite if contents differ | Binary comparison then `os.replace` or `os.unlink` |

## Common Patterns
```python
# Recursive stats with os.walk + extension grouping
import os

def statfile(file_path):
    _, ext = os.path.splitext(file_path)
    ext = os.path.normcase(ext) or "<none>"
    # Count files, bytes, lines, words per extension

def statdir(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            statfile(os.path.join(root, name))

# File organization by extension
mapping = {".pdf": "pdf_files", ".jpg": "image_files", ".py": "python_files"}
for fname in os.listdir("."):
    ext = os.path.splitext(fname)[1].lower()
    if ext in mapping:
        shutil.move(fname, os.path.join(mapping[ext], fname))

# Smart update: only replace if different
with open(old, "rb") as f: old_data = f.read()
with open(new, "rb") as f: new_data = f.read()
if old_data != new_data:
    os.replace(new, old)  # atomic
else:
    os.unlink(new)         # discard
```

## Now Build Your Own
**Challenge:** Write a `watcher.py` that monitors a directory for new files and auto-organizes them into type folders. Use `os.walk` to scan periodically (every 2 seconds), compare with a `set` of known files, and move any new files into the correct `image_files/`, `doc_files/`, etc. Print each move to the console. Stop on Ctrl+C.
