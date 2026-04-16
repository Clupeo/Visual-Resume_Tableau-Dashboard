"""Data Import Module - Handles importing data from Excel into PostgreSQL."""

from pathlib import Path
from typing import List
import pandas as pd
from config import Config
from .database import DatabaseManager


class DataImporter:
    """Handles Excel data import to PostgreSQL."""
    
    TABLE_ORDER: List[str] = [
        "person", "domain", "activity", "activity_domain",
        "certificates", "certificates_domain", "portfolio", "portfolio_domain",
        "skills", "person_skills", "portfolio_skills",
        "tools", "person_tools", "portfolio_tools",
        "languages", "languages_proficiency", "person_languages",
    ]
    
    @staticmethod
    def import_from_excel(excel_path: Path = None) -> None:
        """Import data from Excel to PostgreSQL database."""
        if excel_path is None:
            excel_path = Config.EXCEL_SOURCE_PATH
        
        if not excel_path.exists():
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
        
        db = DatabaseManager()
        db.create_all_tables()
        
        engine = db.get_engine()
        for table_name in DataImporter.TABLE_ORDER:
            try:
                df = pd.read_excel(excel_path, sheet_name=table_name)
                df = df.where(pd.notnull(df), None)
                df.to_sql(table_name, engine, if_exists="append", index=False)
            except ValueError:
                pass
            except Exception as e:
                raise Exception(f"Error importing '{table_name}': {e}")
