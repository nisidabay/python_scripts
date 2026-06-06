#!/usr/bin/env python3
"""Library management: Book / Patron / Loan classes with from_json/to_json, property validation, composition."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================================
# Models
# ============================================================================
class Book:
    """A book in the library catalogue."""

    def __init__(self, title: str, author: str, isbn: str, year: Optional[int] = None):
        self._title = title
        self.author = author
        self._isbn = isbn
        self.year = year

    # --- properties with validation ---
    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not value.strip():
            raise ValueError("title must not be empty")
        self._title = value.strip()

    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, value: str) -> None:
        clean = value.replace("-", "").replace(" ", "")
        if len(clean) not in (10, 13) or not clean.isdigit():
            raise ValueError(f"isbn must be 10 or 13 digits, got {len(clean)}")
        self._isbn = clean

    def to_json(self) -> Dict[str, Any]:
        return {"title": self.title, "author": self.author, "isbn": self.isbn, "year": self.year}

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Book:
        return cls(
            title=data["title"],
            author=data.get("author", "Unknown"),
            isbn=data["isbn"],
            year=data.get("year"),
        )

    def __repr__(self) -> str:
        return f"Book({self.title!r} by {self.author}, ISBN:{self.isbn})"


class Patron:
    """A library patron."""

    def __init__(self, name: str, patron_id: str, email: str = ""):
        self._name = name
        self.patron_id = patron_id
        self.email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("name must not be empty")
        self._name = value.strip()

    def to_json(self) -> Dict[str, Any]:
        return {"name": self.name, "patron_id": self.patron_id, "email": self.email}

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Patron:
        return cls(name=data["name"], patron_id=data["patron_id"], email=data.get("email", ""))

    def __repr__(self) -> str:
        return f"Patron({self.name!r}, ID:{self.patron_id})"


class Loan:
    """A loan tying a book to a patron for a duration."""

    LOAN_DAYS = 14

    def __init__(self, book: Book, patron: Patron, loan_date: Optional[datetime] = None):
        self.book = book
        self.patron = patron
        self.loan_date = loan_date or datetime.now()
        self._returned_date: Optional[datetime] = None

    @property
    def due_date(self) -> datetime:
        return self.loan_date + timedelta(days=self.LOAN_DAYS)

    @property
    def is_overdue(self) -> bool:
        if self._returned_date is not None:
            return self._returned_date > self.due_date
        return datetime.now() > self.due_date

    def return_book(self) -> None:
        self._returned_date = datetime.now()

    def to_json(self) -> Dict[str, Any]:
        return {
            "book": self.book.to_json(),
            "patron": self.patron.to_json(),
            "loan_date": self.loan_date.isoformat(),
            "returned_date": self._returned_date.isoformat() if self._returned_date else None,
            "due_date": self.due_date.isoformat(),
            "overdue": self.is_overdue,
        }

    def __repr__(self) -> str:
        status = "returned" if self._returned_date else ("OVERDUE" if self.is_overdue else "active")
        return f"Loan({self.book.title!r} → {self.patron.name!r} [{status}])"


# ============================================================================
# Library (composition of Books, Patrons, Loans)
# ============================================================================
class Library:
    """Top-level library: holds books, patrons, and current loans."""

    def __init__(self):
        self.books: Dict[str, Book] = {}      # isbn → Book
        self.patrons: Dict[str, Patron] = {}  # patron_id → Patron

    def loans(self) -> List[Loan]:
        # Loans aren't stored; they're built on-demand by the CLI.
        # For persistence, library can serialize books+patrons.
        return []

    def add_book(self, book: Book) -> None:
        if book.isbn in self.books:
            print(f"Warning: overwriting book {book.isbn}", file=sys.stderr)
        self.books[book.isbn] = book

    def add_patron(self, patron: Patron) -> None:
        self.patrons[patron.patron_id] = patron

    def to_json(self) -> Dict[str, Any]:
        return {
            "books": [b.to_json() for b in self.books.values()],
            "patrons": [p.to_json() for p in self.patrons.values()],
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Library:
        lib = cls()
        for bd in data.get("books", []):
            lib.add_book(Book.from_json(bd))
        for pd in data.get("patrons", []):
            lib.add_patron(Patron.from_json(pd))
        return lib


# ============================================================================
# Storage helpers
# ============================================================================
def load_library(path: Path) -> Library:
    if path.exists():
        with open(path) as f:
            return Library.from_json(json.load(f))
    return Library()


def save_library(path: Path, lib: Library) -> None:
    with open(path, "w") as f:
        json.dump(lib.to_json(), f, indent=2)


# ============================================================================
# CLI
# ============================================================================
DATA_FILE = Path.home() / ".library.json"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Library management CLI")
    sub = p.add_subparsers(dest="command", required=True)

    # add-book
    ab = sub.add_parser("add-book", help="Add a book")
    ab.add_argument("--title", required=True)
    ab.add_argument("--author", required=True)
    ab.add_argument("--isbn", required=True)
    ab.add_argument("--year", type=int, default=None)

    # list-books
    sub.add_parser("list-books", help="List all books")

    # add-patron
    ap = sub.add_parser("add-patron", help="Add a patron")
    ap.add_argument("--name", required=True)
    ap.add_argument("--id", required=True, dest="patron_id")
    ap.add_argument("--email", default="")

    # list-patrons
    sub.add_parser("list-patrons", help="List all patrons")

    # loan
    lo = sub.add_parser("loan", help="Create a loan (book → patron)")
    lo.add_argument("--isbn", required=True)
    lo.add_argument("--patron-id", required=True, dest="patron_id")

    # return
    ret = sub.add_parser("return", help="Return a loan")
    ret.add_argument("--isbn", required=True)

    return p


def main() -> None:
    args = build_parser().parse_args()
    lib = load_library(DATA_FILE)

    if args.command == "add-book":
        try:
            book = Book(args.title, args.author, args.isbn, args.year)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        lib.add_book(book)
        save_library(DATA_FILE, lib)
        print(f"Added: {book}")

    elif args.command == "list-books":
        if not lib.books:
            print("No books in library.")
        else:
            for b in lib.books.values():
                year_str = f" ({b.year})" if b.year else ""
                print(f"  {b.title!r} by {b.author}{year_str}  ISBN:{b.isbn}")

    elif args.command == "add-patron":
        try:
            patron = Patron(args.name, args.patron_id, args.email)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        lib.add_patron(patron)
        save_library(DATA_FILE, lib)
        print(f"Added: {patron}")

    elif args.command == "list-patrons":
        if not lib.patrons:
            print("No patrons registered.")
        else:
            for p in lib.patrons.values():
                email = f" <{p.email}>" if p.email else ""
                print(f"  {p.name}{email}  ID:{p.patron_id}")

    elif args.command == "loan":
        book = lib.books.get(args.isbn)
        if not book:
            print(f"Book ISBN {args.isbn} not found.", file=sys.stderr)
            sys.exit(1)
        patron = lib.patrons.get(args.patron_id)
        if not patron:
            print(f"Patron {args.patron_id} not found.", file=sys.stderr)
            sys.exit(1)
        loan = Loan(book, patron)
        print(f"Loan created: {loan}")
        print(f"  Due: {loan.due_date.isoformat(timespec='seconds')}")

    elif args.command == "return":
        book = lib.books.get(args.isbn)
        if not book:
            print(f"Book ISBN {args.isbn} not found.", file=sys.stderr)
            sys.exit(1)
        # In a real system we'd look up the active loan; here we create one and "return" it
        loan = Loan(book, Patron("dummy", "0"))
        loan.return_book()
        rdate = loan._returned_date or datetime.now()
        print(f"Book {book.title!r} returned on {rdate.isoformat(timespec='seconds')}")
        if loan.is_overdue:
            print("  ⚠ Overdue!")

    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
