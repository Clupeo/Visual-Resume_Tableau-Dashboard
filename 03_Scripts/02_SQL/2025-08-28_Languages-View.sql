DROP VIEW IF EXISTS languages_view;

CREATE OR REPLACE VIEW languages_view AS
SELECT 
    l.language_name,
	plv.proficiency_id,
    plv.proficiency_name
FROM person_languages pl
JOIN languages l ON pl.language_id = l.language_id
JOIN languages_proficiency plv ON pl.proficiency_id = plv.proficiency_id
ORDER BY plv.proficiency_id;
