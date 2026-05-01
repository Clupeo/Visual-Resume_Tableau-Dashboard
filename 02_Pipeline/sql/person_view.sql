
DROP VIEW IF EXISTS person_view CASCADE;
CREATE OR REPLACE VIEW person_view AS
SELECT p.person_id, p.title, p.first_name, p.last_name,
       p.city, p.province, p.country, p.birth_date
FROM person p
ORDER BY p.person_id;
        