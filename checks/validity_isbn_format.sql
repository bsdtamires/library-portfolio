-- validity_isbn_format.sql
--
-- Dimension: VALIDITY
-- Convention: this query should return ZERO rows when the data is correct.
--
-- What to check: where `isbn` is set, it should match the shape of a real
-- ISBN. Decide whether you're validating ISBN-13 specifically (13 digits)
-- or accepting ISBN-10 too, and check the pattern with SQLite's LIKE or
-- GLOB operators.

SELECT 'TODO: implement this check' AS status;
