"""
test_checks.py

A generic, check-agnostic test harness — contains NO data validation logic
of its own. It discovers every .sql file in checks/ and runs it against
the database, asserting each returns zero rows (the same convention the
shell/PowerShell runners use, and the same one dbt uses internally). All
13 checks' actual logic lives entirely in their own .sql files — this file
never changes when a check's logic changes, and was written once, not
per-check.

Running this gives a normal pytest report, which VS Code's Testing panel
(and any CI system) already knows how to display — one row per .sql file,
named after the file, individually green or red.
"""
import sqlite3
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "db" / "library.db"
CHECKS_DIR = PROJECT_ROOT / "checks"

CHECK_FILES = sorted(CHECKS_DIR.glob("*.sql"))


@pytest.fixture(scope="session", autouse=True)
def ensure_database_exists():
    if not DB_PATH.exists():
        pytest.exit(
            f"Database not found at {DB_PATH} — run 'python src/seed_data.py' first.",
            returncode=1,
        )


@pytest.mark.parametrize("check_file", CHECK_FILES, ids=lambda f: f.stem)
def test_sql_check(check_file):
    query = check_file.read_text(encoding="utf-8")
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(query).fetchall()
    finally:
        conn.close()
    assert rows == [], f"{check_file.name} returned {len(rows)} offending row(s): {rows[:5]}"
