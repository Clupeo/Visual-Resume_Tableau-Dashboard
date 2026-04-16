
DROP VIEW IF EXISTS filter_view CASCADE;
CREATE OR REPLACE VIEW filter_view AS
SELECT d.domain_id, d.name AS domain_name, d.subtitle AS domain_subtitle,
       d.description AS domain_description, d.hashtags AS domain_hashtags
FROM domain d
WHERE d.name IS NOT NULL
ORDER BY d.name;
        