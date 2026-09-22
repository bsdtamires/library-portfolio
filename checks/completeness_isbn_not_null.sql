-- completeness_isbn_not_null.sql
--
-- Dimension: COMPLETENESS
-- Convention: this query should return ZERO rows when the data is correct.
--
-- What to check: every book should have a non-null `isbn`. A handful of
-- rows are missing one on purpose, standing in for "not catalogued yet."

SELECT * FROM books WHERE isbn IS NULL;