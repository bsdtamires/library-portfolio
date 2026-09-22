#!/usr/bin/env bash
# run_checks.sh
#
# Runs every .sql file in checks/ against db/library.db using the sqlite3
# CLI directly — no Python involved in running the checks themselves.
#
# Convention (same one dbt uses, without needing dbt): each .sql file is a
# SELECT query. Zero rows returned = PASS. Any row returned = FAIL, and
# the returned rows ARE the offending data — that's what makes the failure
# actionable instead of just "check 7 failed."
#
# Usage:
#   bash run_checks.sh
#
# Exits 0 if every check passes, exits 1 if any check fails — this exit
# code is what CI/CD will key off of later.

set -uo pipefail
# Not using -e on purpose: a single failing check should not stop the
# script from running the rest and reporting a full result.

DB_PATH="db/library.db"
CHECKS_DIR="checks"

if [[ ! -f "$DB_PATH" ]]; then
  echo "Database not found at $DB_PATH — run 'python src/seed_data.py' first."
  exit 1
fi

pass_count=0
fail_count=0

for check_file in "$CHECKS_DIR"/*.sql; do
  name=$(basename "$check_file")
  result=$(sqlite3 "$DB_PATH" < "$check_file")

  if [[ -z "$result" ]]; then
    echo "PASS  $name"
    pass_count=$((pass_count + 1))
  else
    echo "FAIL  $name"
    echo "$result" | sed 's/^/      /'
    fail_count=$((fail_count + 1))
  fi
done

echo ""
echo "$pass_count passed, $fail_count failed"

if [[ "$fail_count" -gt 0 ]]; then
  exit 1
fi
exit 0
