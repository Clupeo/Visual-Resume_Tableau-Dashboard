
DROP VIEW IF EXISTS portfolio_view CASCADE;
CREATE OR REPLACE VIEW portfolio_view AS
SELECT DISTINCT
    p.portfolio_id, p.person_id, p.title AS project_title, p.description AS project_description,
    p.start_date AS project_start, p.end_date AS project_end, p.link AS project_link,
    COALESCE(d.domain_id, 0) AS domain_id, COALESCE(d.name, '') AS domain_name,
    COALESCE(s.skill_id, 0) AS skill_id, COALESCE(s.name, '') AS skill_name,
    COALESCE(s.category, '') AS skill_category, COALESCE(s.description, '') AS skill_description,
    CAST(COALESCE(0, 0) AS INTEGER) AS skill_proficiency,
    COALESCE(t.tool_id, 0) AS tool_id, COALESCE(t.name, '') AS tool_name,
    COALESCE(t.category, '') AS tool_category, COALESCE(t.description, '') AS tool_description,
    CAST(COALESCE(0, 0) AS INTEGER) AS tool_proficiency
FROM portfolio p
LEFT JOIN portfolio_domain pd ON pd.portfolio_id = p.portfolio_id
LEFT JOIN domain d ON d.domain_id = pd.domain_id
LEFT JOIN portfolio_skills psx ON psx.portfolio_id = p.portfolio_id
LEFT JOIN skills s ON s.skill_id = psx.skill_id
LEFT JOIN portfolio_tools ptx ON ptx.portfolio_id = p.portfolio_id
LEFT JOIN tools t ON t.tool_id = ptx.tool_id
ORDER BY p.end_date DESC NULLS LAST;
        