DROP VIEW IF EXISTS filter_view;

CREATE OR REPLACE VIEW filter_view AS
SELECT DISTINCT
    d.domain_id,
    d.name AS domain_name,
	d.subtitle AS domain_subtitle,
	d.description AS domain_description,
	d.hashtags AS domain_hashtags
FROM domain d;