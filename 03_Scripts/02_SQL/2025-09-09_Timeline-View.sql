DROP VIEW IF EXISTS timeline_view;

CREATE OR REPLACE VIEW timeline_view AS
SELECT
    a.activity_id,
    a.person_id,
    a.title AS activity_title,
    a.organization,
    a.start_date,
    a.end_date,
    array_agg(d.name) AS domain_name  -- optional, for highlighting
FROM activity a
LEFT JOIN activity_domain ad ON ad.activity_id = a.activity_id
LEFT JOIN domain d ON d.domain_id = ad.domain_id
GROUP BY 
	a.activity_id,
    a.person_id,
    a.title,
    a.organization,
    a.start_date,
    a.end_date;
