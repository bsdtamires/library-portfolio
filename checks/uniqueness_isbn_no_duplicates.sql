-- uniqueness_isbn_no_duplicates.sql
--
-- Dimension: UNIQUENESS
-- Convention: this query should return ZERO rows when the data is correct.
--
-- What to check: each non-null `isbn` should appear at most once. Two
-- rows sharing an ISBN likely means the same book was entered twice.
-- Hint: GROUP BY + HAVING COUNT(*) > 1 is the standard SQL pattern here.

SELECT 'TODO: implement this check' AS status;
