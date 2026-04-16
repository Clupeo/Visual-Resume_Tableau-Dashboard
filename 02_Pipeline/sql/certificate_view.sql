
DROP VIEW IF EXISTS certificate_view CASCADE;
CREATE OR REPLACE VIEW certificate_view AS
SELECT DISTINCT ce.certificate_id, ce.name AS certificate_name, ce.place AS certificate_location,
       ce.issue_date AS certificate_issuedate, ce.image AS certificate_image,
       COALESCE(d.domain_id, 0) AS domain_id, COALESCE(d.name, '') AS domain_name
FROM certificates ce
LEFT JOIN certificates_domain cd ON cd.certificate_id = ce.certificate_id
LEFT JOIN domain d ON d.domain_id = cd.domain_id
ORDER BY ce.issue_date DESC NULLS LAST;
        