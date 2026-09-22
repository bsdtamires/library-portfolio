-- completeness_title_not_null.sql
--
-- Dimension: COMPLETENESS
-- Convention: this query should return ZERO rows when the data is correct.
-- Any row returned is a violation — return enough columns to identify
-- exactly which book failed without re-querying.
--
-- What to check: every book should have a non-null, non-empty `title`.
-- A blank title makes the record useless for browsing the library.

SELECT * FROM books WHERE title IS NULL;
