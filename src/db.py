"""
db.py

Minimal data-access helper. This file's job is to *retrieve* data — it makes
no judgment about whether the data is good or bad. That judgment belongs in
the test files, not here.
"""
import sqlite3


def fetch_all_books(db_path: str) -> list[dict]:
    """Return every row in the books table as a list of dicts."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(
            "SELECT id, title, author, isbn, genre, publication_year, "
            "date_acquired, read_status, rating, format, pages FROM books "
            "ORDER BY id"
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
