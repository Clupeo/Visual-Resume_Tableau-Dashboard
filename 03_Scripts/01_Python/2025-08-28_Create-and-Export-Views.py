import os
import glob
import shutil
from sqlalchemy import create_engine, text
from datetime import date

# -----------------
# CONFIG (same as schema_setup.py)
# -----------------
db_user = "postgres"
db_password = "#01805#SQL#"
db_host = "localhost"
db_port = "5432"
db_name = "Dashboard_Resume"

# -----------------
# DB CONNECTION
# -----------------
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# -----------------
# EXECUTE ALL SQL FILES
# -----------------
sql_path = "02_SQL"  # folder where your .sql files are stored
sql_files = sorted(glob.glob(os.path.join(sql_path, "*.sql")))
print(sql_files)
with engine.connect() as conn:
    for filepath in sql_files:
        print(f"📄 Running {filepath}...")
        with open(filepath, "r", encoding="utf-8") as f:
            sql = f.read()
            try:
                conn.execute(text(sql))
                print(f"✅ Executed {os.path.basename(filepath)}")
            except Exception as e:
                print(f"❌ Error in {filepath}: {e}")
    conn.commit()

# -----------------
# EXPORT TO EXCEL
# -----------------
import pandas as pd

# Today's date for filenames
#date_prefix = date.today().strftime("%Y-%m-%d")
date_prefix = "2025-09-10"

# create this exports folder, if necessary
output_folder = "./03_Exports"  
os.makedirs(output_folder, exist_ok=True)

choice = input("Delete or Archive files? (d/a): ").strip().lower()

# Delete all files
if choice == "d":
    for f in glob.glob(os.path.join(output_folder, "*")):
        os.remove(f)
    print(f"🗑 Cleared {output_folder} folder before export.")

# Clear all existing files in the exports folder
else:
    archive_folder = os.path.join(output_folder, "../../99_Archive/Database-Output")
    os.makedirs(archive_folder, exist_ok=True)  # ensure archive folder exists

    for f in glob.glob(os.path.join(output_folder, "*")):
        if os.path.isfile(f):  # only move files, not directories
            shutil.move(f, archive_folder)

    print(f"📦 Moved files from {output_folder} to {archive_folder}")

# -----------------
# List of tables (or queries) to export
# -----------------
views = {"person_view", "languages_view", "timeline_view", "portfolio_view", "certificate_view", "filter_view"}

# -----------------
# EXPORT ALL TABLES AND QUERIES
# -----------------
with engine.connect() as conn:
    for view_name in views:
        print(f"⬇ Exporting {view_name} to Excel...")
        df = pd.read_sql(f"SELECT * FROM {view_name};", conn)
        file_path = os.path.join(output_folder, f"{date_prefix}_{view_name}.xlsx")
        df.to_excel(file_path, sheet_name=view_name, index=False)

print("🎉 All views exported to Excel files.")


