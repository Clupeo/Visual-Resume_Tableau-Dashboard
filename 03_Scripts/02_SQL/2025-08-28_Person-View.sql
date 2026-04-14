DROP VIEW IF EXISTS person_view;

CREATE OR REPLACE VIEW person_view AS
SELECT 
    p.person_id,
    p.title,
    p.first_name,
    p.last_name,
    p.city,
    p.province,
    p.country,
    p.birth_date
FROM person p;