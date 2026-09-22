-- completeness_author_not_null.sql
--
-- Dimension: COMPLETENESS
-- Convention: this query should return ZERO rows when the data is correct.
--
-- What to check: every book should have a non-null, non-empty `author`.

SELECT * FROM books WHERE author IS NULL;
