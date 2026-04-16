
DROP VIEW IF EXISTS timeline_view CASCADE;
CREATE OR REPLACE VIEW timeline_view AS
SELECT a.activity_id, a.person_id, a.title AS activity_title, a.organization,
       a.start_date, a.end_date,
       ARRAY_AGG(DISTINCT d.name ORDER BY d.name) FILTER (WHERE d.name IS NOT NULL) AS domain_name
FROM activity a
LEFT JOIN activity_domain ad ON ad.activity_id = a.activity_id
LEFT JOIN domain d ON d.domain_id = ad.domain_id
GROUP BY a.activity_id, a.person_id, a.title, a.organization, a.start_date, a.end_date
ORDER BY a.start_date DESC NULLS LAST;
        