# Personal Library — Data Quality Validation (SQL-only)

A SQLite database of my personal book collection (140 books — real titles
and authors, fabricated enrichment data), paired with data quality checks
written as **plain SQL**, run three different ways depending on context.

**Status: schema and data loaded, check scaffolding built, check logic in
progress.** Every file in `checks/` is a stub — a header comment describing
what to verify, and a placeholder query. The actual validation SQL is
being written by me, deliberately, as a learning exercise.

## What's real and what's fabricated, and why

`title` and `author` are my real 140 books, unchanged. Every other column
— `isbn`, `genre`, `publication_year`, `date_acquired`, `read_status`,
`rating`, `format`, `pages` — is fabricated test data
(`scripts/generate_dummy_data.py`), deliberately seeded with nulls,
duplicates, out-of-range values, and bad formats, so the checks have real,
known issues to catch. This is clearly labeled fabrication, not a claim
about my actual reading history — `data/books_real_only.csv` keeps the
unmodified real list for provenance.

## Why SQL-only, not pytest-as-the-logic, not dbt

SQL is my strongest skill; Python is one I'm actively building. The
validation *logic* is 100% SQL — no framework decides what "correct"
means, a `SELECT` query does. dbt is the industry-standard tool for
exactly this pattern; I considered it and deliberately didn't reintroduce
it here, since I'd already scoped it out of my current learning roadmap.

## Three ways to run the checks

**1. VS Code Testing panel** (recommended day to day):
- Install the Python extension if you don't have it already.
- `Ctrl+Shift+P` → "Python: Configure Tests" → choose **pytest** → choose
  the project root.
- Open the Testing icon (flask/beaker) in the left sidebar. You'll see 13
  tests, one per check file, named after the file. Click the play button
  to run all of them, or any single one — pass/fail shows inline, per
  check, no terminal reading required.

**2. Command line, any OS:**
```bash
pip install -r requirements.txt
python src/seed_data.py
pytest tests/ -v
```

**3. Shell scripts** (no Python test framework involved at all — useful
for CI, or if you just want raw terminal output):
```bash
bash run_checks.sh        # Git Bash / Mac / Linux
.\run_checks.ps1          # native Windows PowerShell
```

All three run the exact same `.sql` files and apply the exact same
pass/fail rule — they're three different reporting layers on top of one
set of checks, not three different sets of logic.

## The convention every check follows

Each file in `checks/` holds exactly **one** `SELECT` statement:

- **Zero rows returned → PASS.**
- **Any row returned → FAIL**, and the row(s) are the actual offending
  data.

Important: a check file must contain exactly one SQL statement. When you
implement a check, **replace** the placeholder line — don't add your real
query below it, or the runner will error rather than run either one.

## The four data quality dimensions

- **Completeness** (`completeness_*.sql`, 3 files)
- **Validity** (`validity_*.sql`, 5 files)
- **Consistency** (`consistency_*.sql`, 4 files)
- **Uniqueness** (`uniqueness_*.sql`, 1 file)

## Project structure

```
data/
  books_real_only.csv   — my real 140 books, title/author only, untouched
  books.csv             — real title/author + fabricated enrichment (what actually loads)
scripts/
  generate_dummy_data.py — one-time generator that produced books.csv; kept for transparency
src/
  seed_data.py           — loads books.csv, builds the schema
  db.py                  — retrieves data only; makes no judgment about it
checks/
  completeness_*.sql, validity_*.sql, consistency_*.sql, uniqueness_*.sql
  — 13 stub checks, not yet implemented
tests/
  test_checks.py         — generic pytest harness; discovers and runs every checks/*.sql
                            file, contains no validation logic of its own
run_checks.sh            — CLI runner, Git Bash / Mac / Linux / CI
run_checks.ps1           — CLI runner, native Windows PowerShell
```

## Next step

Once the checks are implemented and passing, this suite runs automatically
in CI/CD via GitHub Actions on every push — in progress.
