-- consistency_unread_has_no_rating.sql
--
-- Dimension: CONSISTENCY
-- Convention: this query should return ZERO rows when the data is correct.
--
-- What to check: business rule — a book marked "unread" shouldn't have a
-- rating. Find any row where read_status is unread AND rating is not null.

SELECT 'TODO: implement this check' AS status;
