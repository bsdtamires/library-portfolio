"""
generate_dummy_data.py

ONE-TIME utility, not part of the ongoing pipeline. Takes the real
title/author list and adds fabricated values for the other 8 columns
(isbn, genre, publication_year, date_acquired, read_status, rating,
format, pages) — deliberately including nulls, duplicates, bad formats,
and out-of-range values, spread across the columns, so every one of the
13 SQL checks has real, known data to catch.

This script is run once to produce data/books.csv. It is not re-run as
part of seeding — seed_data.py just loads whatever is in that CSV.
Kept in the repo for transparency: this is how the dummy data was made,
and it's honestly labeled as fabricated, not represented as real.
"""
import csv
import random
from pathlib import Path

random.seed(42)  # reproducible output

SOURCE_CSV = Path(__file__).parent.parent / "data" / "books_real_only.csv"
OUTPUT_CSV = Path(__file__).parent.parent / "data" / "books.csv"

GENRES = [
    "Fiction", "Non-fiction", "Fantasy", "Science Fiction", "Mystery",
    "Romance", "Biography", "Self-help", "History", "Thriller",
    "Classic", "Young Adult", "Graphic Novel", "Poetry",
]
VALID_READ_STATUS = ["unread", "reading", "read"]
VALID_FORMAT = ["physical", "ebook", "audiobook"]


def random_isbn():
    return "978" + "".join(str(random.randint(0, 9)) for _ in range(10))


def random_date(start_year=2015, end_year=2026):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year:04d}-{month:02d}-{day:02d}"


def generate_rows(real_books: list[dict]) -> list[dict]:
    rows = []
    duplicate_isbn_pool = []

    for i, book in enumerate(real_books):
        row = {
            "title": book["title"],
            "author": book["author"],
            "isbn": random_isbn(),
            "genre": random.choice(GENRES),
            "publication_year": random.randint(1950, 2025),
            "date_acquired": random_date(),
            "read_status": random.choices(
                VALID_READ_STATUS, weights=[15, 10, 75]
            )[0],
            "rating": None,
            "format": random.choices(
                VALID_FORMAT, weights=[70, 20, 10]
            )[0],
            "pages": random.randint(120, 650),
        }
        if row["read_status"] == "read":
            row["rating"] = random.randint(1, 5)
        rows.append(row)

    # --- deliberately inject known issues into a subset of rows ---

    # completeness: 8 rows missing isbn
    for idx in random.sample(range(len(rows)), 8):
        rows[idx]["isbn"] = None

    # validity: 3 rows with a future publication_year
    for idx in random.sample(range(len(rows)), 3):
        rows[idx]["publication_year"] = random.randint(2027, 2030)

    # validity: 3 rows with non-positive pages
    for idx in random.sample(range(len(rows)), 3):
        rows[idx]["pages"] = random.choice([0, -12])

    # validity: 3 rows with rating out of the 1-5 scale
    for idx in random.sample(range(len(rows)), 3):
        if rows[idx]["rating"] is None:
            rows[idx]["read_status"] = "read"
        rows[idx]["rating"] = random.choice([7, 8, 9])

    # validity: 5 rows with a malformed isbn (not null, but wrong shape)
    non_null_isbn_idx = [i for i, r in enumerate(rows) if r["isbn"] is not None]
    for idx in random.sample(non_null_isbn_idx, 5):
        rows[idx]["isbn"] = random.choice([
            "12345",                     # too short
            "978-0-13-595705-9",         # hyphenated, not raw digits
            "97812345678AB",             # contains letters
        ])

    # validity: 4 rows with a malformed date_acquired
    for idx in random.sample(range(len(rows)), 4):
        d = rows[idx]["date_acquired"]
        y, m, dd = d.split("-")
        rows[idx]["date_acquired"] = random.choice([
            f"{dd}/{m}/{y}",              # DD/MM/YYYY instead of ISO
            "not a date",
        ])

    # consistency: 3 rows with an unknown read_status value
    for idx in random.sample(range(len(rows)), 3):
        rows[idx]["read_status"] = random.choice(["Read", "finished", ""])

    # consistency: 3 rows with an unknown format value
    for idx in random.sample(range(len(rows)), 3):
        rows[idx]["format"] = random.choice(["Physical", "kindle", "audiobok"])

    # consistency: 3 unread books that still have a rating
    unread_idx = [i for i, r in enumerate(rows) if r["read_status"] == "unread"]
    for idx in random.sample(unread_idx, min(3, len(unread_idx))):
        rows[idx]["rating"] = random.randint(1, 5)

    # consistency: 4 read books with no rating
    read_idx = [i for i, r in enumerate(rows) if r["read_status"] == "read"]
    for idx in random.sample(read_idx, min(4, len(read_idx))):
        rows[idx]["rating"] = None

    # uniqueness: 3 pairs of rows sharing the same isbn
    non_null_isbn_idx = [i for i, r in enumerate(rows) if r["isbn"] is not None]
    chosen = random.sample(non_null_isbn_idx, 6)
    for a, b in zip(chosen[0::2], chosen[1::2]):
        rows[b]["isbn"] = rows[a]["isbn"]

    return rows


def main():
    with open(SOURCE_CSV, newline="", encoding="utf-8") as f:
        real_books = list(csv.DictReader(f))

    rows = generate_rows(real_books)

    fieldnames = [
        "title", "author", "isbn", "genre", "publication_year",
        "date_acquired", "read_status", "rating", "format", "pages",
    ]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Generated {len(rows)} rows with fabricated enrichment data -> {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
