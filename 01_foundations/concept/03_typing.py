#!/usr/bin/env python3
# Type hints that catch bugs before runtime — static analysis for Python.

from typing import Optional, Union, List, Dict, Literal, Protocol, TypeAlias
from dataclasses import dataclass

# Literal: restrict to exact string/int values — great for flags
Level = Literal["debug", "info", "warning", "error"]  # 4 choices, nothing else

# TypeAlias: give semantic names to type expressions
UserId: TypeAlias = int  # clearer than raw int everywhere
Scores: TypeAlias = Dict[UserId, List[int]]  # nested structure with meaning

# Optional[X] is Union[X, None] — explicit about nullability
def get_score(scores: Scores, uid: UserId) -> Optional[int]:
    """Latest score or None if user unseen."""
    user_scores = scores.get(uid)
    return user_scores[-1] if user_scores else None

# Union: this OR that — use when multiple types are valid
def format_id(identifier: Union[int, str]) -> str:
    return f"ID-{identifier:0>6}" if isinstance(identifier, int) else identifier

# Protocol: structural subtyping — "if it quacks like a duck..."
class Named(Protocol):
    name: str  # any object with a .name attribute satisfies this

def greet(entity: Named) -> str:
    return f"Hello, {entity.name}"

@dataclass
class Person:
    name: str
    age: int

# Demonstrate usage
scores_db: Scores = {1: [85, 92], 2: [78]}  # type-annotated variable
latest = get_score(scores_db, 1)  # Optional[int] — mypy enforces None check
if latest is not None:
    print(f"Latest score: {latest}")

p = Person(name="Carlos", age=34)
print(greet(p))  # Person satisfies Named protocol

level: Level = "info"  # Literal catches typos at type-check time
print(format_id(42), format_id("ABC"))

# reveal_type pattern: mypy shows inferred type when it sees this
# Uncomment the next line and run: mypy 03_typing.py
# reveal_type(scores_db)

if __name__ == "__main__":
    assert get_score(scores_db, 99) is None, "Missing user should return None"
    print("typing checks passed")
