DROP VIEW IF EXISTS portfolio_view;

CREATE OR REPLACE VIEW portfolio_view AS
SELECT
    p.portfolio_id,
    p.person_id,
    p.title AS project_title,
    p.description AS project_description,
    p.start_date AS project_start,
    p.end_date AS project_end,
    p.link AS project_link,

	-- Domains
    d.domain_id,
	d.name AS domain_name,

	-- Skills
    s.skill_id,
    s.name AS skill_name,
	s.category AS skill_category,
	s.description AS skill_description,
    ps.proficiency_level AS skill_proficiency,

	-- Tools
    t.tool_id,
    t.name AS tool_name,
	t.category AS tool_category,
	t.description AS tool_description,
    pt.proficiency_level AS tool_proficiency
	
FROM portfolio p
LEFT JOIN portfolio_domain pd ON pd.portfolio_id = p.portfolio_id
LEFT JOIN domain d ON d.domain_id = pd.domain_id

-- Skills
LEFT JOIN portfolio_skills psx ON psx.portfolio_id = p.portfolio_id
LEFT JOIN skills s ON s.skill_id = psx.skill_id
LEFT JOIN person_skills ps ON ps.person_id = p.person_id AND ps.skill_id = s.skill_id

-- Tools
LEFT JOIN portfolio_tools ptx ON ptx.portfolio_id = p.portfolio_id
LEFT JOIN tools t ON t.tool_id = ptx.tool_id
LEFT JOIN person_tools pt ON pt.person_id = p.person_id AND pt.tool_id = t.tool_id;
