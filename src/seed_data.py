"""
seed_data.py

Builds the SQLite database for a personal book library, from a real data
file: data/books.csv —  actual 140 books (title, author), exported from
my spreadsheet.

One correction was made during import: one book ("Todo mundo tem uma
primeira vez", an anthology) had a 6th author that had spilled into a
separate, unnamed column in the original spreadsheet instead of being
listed with the other five. That name has been merged back into the author
field here, because the goal of this database is to accurately represent
your real books — manufacturing a test case by leaving an author's name
out would mean the data was simply wrong. One real formatting
inconsistency was deliberately left untouched: one author entry
("Aya de Yopougon") still carries a leftover "(Autor)" role-label,
inconsistent with every other entry in the file.

The schema includes several columns beyond title/author — isbn, genre,
publication_year, date_acquired, read_status, rating, format, pages —
that don't exist in your real source data. Those columns are filled with
FABRICATED values (see scripts/generate_dummy_data.py), deliberately
including nulls, duplicates, out-of-range values, and bad formats, so the
SQL checks in checks/ have real, known issues to catch. Title and author
are the only genuinely real fields in this dataset — everything else is
clearly-labeled synthetic test data, not a claim about your actual books.
"""
import csv
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DB_DIR = PROJECT_ROOT / "db"
DB_PATH = DB_DIR / "library.db"
BOOKS_CSV = PROJECT_ROOT / "data" / "books.csv"

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    isbn TEXT,
    genre TEXT,
    publication_year INTEGER,
    date_acquired TEXT,
    read_status TEXT,
    rating INTEGER,
    format TEXT,
    pages INTEGER
);
"""


def load_books_from_csv() -> list[tuple]:
    """Read every column from data/books.csv, converting blanks to real NULLs."""
    def clean(value):
        return value if value not in (None, "") else None

    def clean_int(value):
        value = clean(value)
        return int(value) if value is not None else None

    rows = []
    with open(BOOKS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            rows.append((
                i,
                clean(row["title"]),
                clean(row["author"]),
                clean(row["isbn"]),
                clean(row["genre"]),
                clean_int(row["publication_year"]),
                clean(row["date_acquired"]),
                clean(row["read_status"]),
                clean_int(row["rating"]),
                clean(row["format"]),
                clean_int(row["pages"]),
            ))
    return rows


def build_db() -> int:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    rows = load_books_from_csv()

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(SCHEMA)
        conn.executemany(
            "INSERT INTO books (id, title, author, isbn, genre, publication_year, "
            "date_acquired, read_status, rating, format, pages) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )
        conn.commit()
    finally:
        conn.close()

    return len(rows)


def seed() -> None:
    count = build_db()
    print(f"Seeded {count} real books into {DB_PATH}")


if __name__ == "__main__":
    seed()
