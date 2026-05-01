"""
Configuration Module for Visual Resume Dashboard
================================================

Handles all environment variables and configuration settings.
Provides centralized configuration management for database, data sources, and exports.

Design Principles:
- Single source of truth for all configuration
- Environment-based (dev/production settings)
- Type-safe with validation
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (with explicit path)
PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)


class Config:
    """Base configuration class with all required settings."""
    
    # Database Configuration
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "Dashboard_Resume")
    
    # Data Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    EXCEL_SOURCE_PATH: Path = PROJECT_ROOT / os.getenv(
        "EXCEL_SOURCE_PATH", 
        "01_Data/raw/master_database.xlsx"
    )
    EXPORT_FOLDER: Path = PROJECT_ROOT / os.getenv(
        "EXPORT_FOLDER",
        "02_Pipeline/outputs"
    )
    SQL_FOLDER: Path = PROJECT_ROOT / "02_Pipeline/sql"
    EXCEL_OUTPUT_FILENAME: str = "visual-Resume_dashboard-data.xlsx"
    
    # Google Sheets Configuration (Optional)
    GOOGLE_SHEETS_ID: str = os.getenv("GOOGLE_SHEETS_ID", "")
    GOOGLE_CREDENTIALS_PATH: str = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
    
    @classmethod
    def get_database_url(cls) -> str:
        """
        Construct PostgreSQL connection URL.
        
        Returns:
            str: PostgreSQL connection string for SQLAlchemy
        """
        return (
            f"postgresql+psycopg2://{cls.DB_USER}:{cls.DB_PASSWORD}"
            f"@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        )
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate critical configuration values.
        
        Returns:
            bool: True if all critical configs are valid
            
        Raises:
            ValueError: If critical configuration is missing
        """
        if not cls.DB_PASSWORD:
            raise ValueError(
                "❌ DB_PASSWORD not set. Please configure .env file or environment variables."
            )
        if not cls.EXCEL_SOURCE_PATH.exists():
            raise ValueError(
                f"❌ Excel source not found: {cls.EXCEL_SOURCE_PATH}\n"
                f"   Expected at: {cls.EXCEL_SOURCE_PATH.absolute()}"
            )
        return True
    
    @classmethod
    def ensure_export_folder(cls) -> None:
        """Create export folder if it doesn't exist."""
        cls.EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # Test configuration on import
    print("📋 Configuration loaded:")
    print(f"   Database: {Config.DB_NAME} @ {Config.DB_HOST}:{Config.DB_PORT}")
    print(f"   Excel Source: {Config.EXCEL_SOURCE_PATH}")
    print(f"   Export Folder: {Config.EXPORT_FOLDER}")
    print(f"   SQL Folder: {Config.SQL_FOLDER}")
    print(f"   Google Sheets ID: {'✅ Set' if Config.GOOGLE_SHEETS_ID else '⚠️  Not set (optional)'}")
    print(f"   Google Credentials: {Config.GOOGLE_CREDENTIALS_PATH}")
