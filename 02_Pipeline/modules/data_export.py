"""Data Export Module - Handles executing SQL views and exporting to Excel."""

import shutil
from pathlib import Path
from typing import Set, Optional
import pandas as pd
from sqlalchemy import text

from config import Config
from .database import DatabaseManager


def ask_for_confirmation(message: str) -> bool:
    """
    Ask user for Y/N confirmation.
    
    Args:
        message: The confirmation message to display
        
    Returns:
        bool: True if user enters 'Y' or 'y', False if 'N' or 'n', re-asks otherwise
    """
    while True:
        response = input(f"\n{message} (Y/N): ").strip().upper()
        if response == "Y":
            return True
        elif response == "N":
            return False
        else:
            print("   ⚠️  Please enter 'Y' or 'N'")


class DataExporter:
    """Handles SQL view execution and Excel export."""
    
    EXPORT_VIEWS: Set[str] = {
        "portfolio_view",
        "timeline_view",
        "certificate_view",
        "filter_view",
    }
    
    # SQL view definitions (embedded so pipeline works even if .sql files are deleted)
    SQL_VIEWS = {
        "portfolio_view": """
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
        """,
        
        "timeline_view": """
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
        """,
        
        "certificate_view": """
DROP VIEW IF EXISTS certificate_view CASCADE;
CREATE OR REPLACE VIEW certificate_view AS
SELECT DISTINCT ce.certificate_id, ce.name AS certificate_name, ce.place AS certificate_location,
       ce.issue_date AS certificate_issuedate, ce.image AS certificate_image,
       COALESCE(d.domain_id, 0) AS domain_id, COALESCE(d.name, '') AS domain_name
FROM certificates ce
LEFT JOIN certificates_domain cd ON cd.certificate_id = ce.certificate_id
LEFT JOIN domain d ON d.domain_id = cd.domain_id
ORDER BY ce.issue_date DESC NULLS LAST;
        """,
        
        "filter_view": """
DROP VIEW IF EXISTS filter_view CASCADE;
CREATE OR REPLACE VIEW filter_view AS
SELECT d.domain_id, d.name AS domain_name, d.subtitle AS domain_subtitle,
       d.description AS domain_description, d.hashtags AS domain_hashtags
FROM domain d
WHERE d.name IS NOT NULL
ORDER BY d.name;
        """,
    }
    
    @staticmethod
    def check_and_confirm_overwrite() -> bool:
        """
        Check for existing SQL and Excel files before pipeline creates any.
        Ask user for confirmation if files exist.
        
        Returns:
            bool: True if user confirms to overwrite (or no files exist), False if user aborts
        """
        existing_files = list(Config.EXPORT_FOLDER.glob("*.xlsx")) if Config.EXPORT_FOLDER.exists() else []
        sql_files = list(Config.SQL_FOLDER.glob("*.sql")) if Config.SQL_FOLDER.exists() else []
        
        # If no files exist, proceed without asking
        if not existing_files and not sql_files:
            return True
        
        # Files exist, ask for confirmation
        files_info = []
        if existing_files:
            files_info.append(f"   📊 Excel files in outputs/: {len(existing_files)} files")
        if sql_files:
            files_info.append(f"   📝 SQL files in sql/: {len(sql_files)} files")
        
        print("\n   ⚠️  Existing files detected:")
        for info in files_info:
            print(info)
        
        return ask_for_confirmation("   Do you want to overwrite these files?")
    
    @staticmethod
    def execute_sql_views() -> None:
        """Execute SQL view creation scripts and save them to sql folder."""
        db = DatabaseManager()
        sql_folder = Config.SQL_FOLDER
        
        # Ensure sql folder exists
        sql_folder.mkdir(parents=True, exist_ok=True)
        
        engine = db.get_engine()
        with engine.connect() as conn:
            # Use embedded SQL view definitions and save them
            for view_name in DataExporter.EXPORT_VIEWS:
                if view_name in DataExporter.SQL_VIEWS:
                    sql_query = DataExporter.SQL_VIEWS[view_name]
                    conn.execute(text(sql_query))
                    conn.commit()
                    
                    # Save the SQL to file in sql folder
                    sql_file_path = sql_folder / f"{view_name}.sql"
                    with open(sql_file_path, "w", encoding="utf-8") as f:
                        f.write(sql_query)
    
    @staticmethod
    def export_views_to_excel(views: Optional[Set[str]] = None) -> None:
        """Export SQL views to Excel files."""
        views = views or DataExporter.EXPORT_VIEWS
        db = DatabaseManager()
        
        Config.ensure_export_folder()
        
        # Clear existing Excel exports
        if Config.EXPORT_FOLDER.exists():
            for f in Config.EXPORT_FOLDER.glob("*.xlsx"):
                f.unlink()
        
        engine = db.get_engine()
        with engine.connect() as conn:
            for view_name in sorted(views):
                df = pd.read_sql(f"SELECT * FROM {view_name};", conn)
                filename = f"{view_name}.xlsx"
                file_path = Config.EXPORT_FOLDER / filename
                df.to_excel(file_path, sheet_name=view_name, index=False)
