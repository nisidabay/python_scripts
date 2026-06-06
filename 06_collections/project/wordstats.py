#!/usr/bin/env python3
"""Word frequency analyzer: Counter, defaultdict, ChainMap for aliases, namedtuple for results.

Reads text, outputs statistics — stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict, ChainMap
from pathlib import Path
from typing import Dict, Iterator, List, NamedTuple, Optional, Set


# ---------------------------------------------------------------------------
# Named tuple for results
# ---------------------------------------------------------------------------
class WordStats(NamedTuple):
    word: str
    frequency: int
    pct: float


# ---------------------------------------------------------------------------
# Word extraction
# ---------------------------------------------------------------------------
def extract_words(text: str) -> Iterator[str]:
    """Yield lowercase words from text, stripping punctuation."""
    for m in re.finditer(r"\b[a-zA-Z]+\b", text):
        yield m.group().lower()


# ---------------------------------------------------------------------------
# Aliases / stop-words via ChainMap
# ---------------------------------------------------------------------------
_DEFAULT_STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "shall", "i", "you", "he", "she",
    "it", "we", "they", "me", "him", "her", "us", "them", "my", "your",
    "his", "its", "our", "their", "this", "that", "these", "those",
    "of", "in", "to", "for", "on", "with", "at", "by", "from", "as",
    "into", "through", "during", "before", "after", "above", "below",
    "between", "and", "but", "or", "nor", "not", "so", "yet", "if", "then",
    "than", "too", "very", "just", "about", "also",
}
_DEFAULT_STOP_WORDS = {w.lower() for w in _DEFAULT_STOP_WORDS}


def load_custom_stopwords(path: Optional[Path]) -> Set:
    """Load user-defined stop-words from file (one per line)."""
    if not path or not path.exists():
        return set()
    with open(path) as f:
        return {line.strip().lower() for line in f if line.strip()}


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def analyze(
    paths: List[Path],
    stopwords_file: Optional[Path] = None,
    top_n: int = 20,
    include_stopwords: bool = False,
) -> List[WordStats]:
    """Return top-N word frequencies from the given files."""
    counter: Counter = Counter()
    # defaultdict for per-file word counts
    per_file: Dict[str, Counter] = defaultdict(Counter)

    all_text = ""
    for p in paths:
        with open(p) as f:
            text = f.read()
        all_text += text + "\n"
        for word in extract_words(text):
            counter[word] += 1
            per_file[str(p)][word] += 1

    # Build stopwords via ChainMap: custom overrides default
    # Convert sets to dicts for ChainMap (ChainMap expects MutableMapping)
    custom = load_custom_stopwords(stopwords_file)
    stopwords_map = ChainMap(
        {w: True for w in custom},
        {w: True for w in _DEFAULT_STOP_WORDS},
    )

    total_words = sum(counter.values())
    if total_words == 0:
        return []

    results = []
    for word, count in counter.most_common():
        if not include_stopwords and word in stopwords_map:
            continue
        results.append(WordStats(word, count, (count / total_words) * 100))  # type: ignore[arg-type]
        if len(results) >= top_n:
            break

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Word frequency analyzer using Counter, defaultdict, ChainMap, namedtuple."
    )
    p.add_argument("files", nargs="+", type=Path, help="Text file(s) to analyze")
    p.add_argument("-n", "--top", type=int, default=20, help="Show top N words (default: 20)")
    p.add_argument("--include-stopwords", action="store_true",
                   help="Include common stop-words in results")
    p.add_argument("--stopwords-file", type=Path, default=None,
                   help="Custom stop-words file (one per line)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    return p


def main() -> None:
    args = build_parser().parse_args()

    # Validate files
    for path in args.files:
        if not path.exists():
            print(f"Error: file not found: {path}", file=sys.stderr)
            sys.exit(1)

    results = analyze(
        paths=args.files,
        stopwords_file=args.stopwords_file,
        top_n=args.top,
        include_stopwords=args.include_stopwords,
    )

    if not results:
        print("No words found.")
        return

    if args.json:
        import json
        print(json.dumps([r._asdict() for r in results], indent=2))
        return

    # Pretty-print table
    max_word = max(len(r.word) for r in results)
    max_count = max(len(str(r.frequency)) for r in results)
    header = f"{'Word':<{max_word}}  {'Count':>{max_count}}  {'%'}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r.word:<{max_word}}  {r.frequency:>{max_count}d}  {r.pct:5.1f}%")

    total = len(results)
    unique = sum(1 for r in results)
    print(f"\nShowing top {total} of {unique} unique words.")


if __name__ == "__main__":
    main()
