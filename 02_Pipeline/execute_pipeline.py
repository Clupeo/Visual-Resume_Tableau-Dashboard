#!/usr/bin/env python3
"""
execute_pipeline.py
===================

Complete ETL pipeline: Import Excel data → Create database → Execute views → Export to Excel.

Usage:
    python execute_pipeline.py

This script does everything in one command:
1. Creates database schema
2. Imports data from Excel
3. Creates SQL views
4. Exports views to Excel files in outputs/ folder AND SQL files to sql/ folder
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from modules import DatabaseManager, DataImporter, DataExporter


def main():
    """Execute complete ETL pipeline."""
    
    print("\n" + "=" * 70)
    print("  Visual Resume Dashboard - ETL Pipeline")
    print("=" * 70 + "\n")
    
    try:
        # Step 1: Validate Configuration
        print("1️⃣  Validating configuration...")
        Config.validate()
        print(f"   ✅ Database: {Config.DB_NAME}")
        print(f"   ✅ Data source: {Config.EXCEL_SOURCE_PATH.name}")
        
        # Step 1b: Check for existing files and ask for confirmation before creating anything
        print("\n1️⃣ᵇ Checking for existing files...")
        if not DataExporter.check_and_confirm_overwrite():
            print("\n   ❌ Pipeline aborted by user.\n")
            return 1
        print("   ✅ Proceeding with pipeline")
        
        # Step 2: Setup Database
        print("\n2️⃣  Setting up database...")
        db = DatabaseManager()
        db.drop_all_tables()
        db.create_all_tables()
        print("   ✅ Database schema created")
        
        # Step 3: Import Data
        print("\n3️⃣  Importing data from Excel...")
        importer = DataImporter()
        importer.import_from_excel()
        print("   ✅ Data imported")
        
        # Step 4: Execute Views
        print("\n4️⃣  Creating SQL views...")
        DataExporter.execute_sql_views()
        print("   ✅ Views created and SQL files saved to sql/ folder")
        
        # Step 5: Export to Excel
        print("\n5️⃣  Exporting views to Excel...")
        DataExporter.export_views_to_excel()
        print("   ✅ Exports complete")
        
        print("\n" + "=" * 70)
        print("  ✅ Pipeline finished successfully!")
        print("=" * 70 + "\n")
        print(f"   📁 Excel outputs: {Config.EXPORT_FOLDER}")
        print(f"   📁 SQL files: {Config.SQL_FOLDER}")
        print("   📊 Files: portfolio_view.xlsx, timeline_view.xlsx, certificate_view.xlsx, filter_view.xlsx\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
