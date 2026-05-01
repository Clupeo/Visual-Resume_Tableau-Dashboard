# Visual Résumé - Tableau Dashboard

Interactive Tableau dashboard showcasing professional expertise, career timeline, skills, and portfolio projects. A data-driven alternative to traditional resumes.

Live Dashboard: [Tableau Public](https://public.tableau.com/app/profile/cedric.hering.peter/viz/CV-Dashboard_17551211549430/Published_Apr-26?publish=yes)

---

## Prerequisites

Before you start, ensure you have:

- **PostgreSQL 12+** - Download from [postgresql.org](https://www.postgresql.org/)
- **Git** - For cloning the repository
- **Python 3.10+** - Download from [python.org](https://www.python.org/)
- **Tableau Desktop or Public account** - Get from [tableau.com](https://www.tableau.com/)

---

## Quick Start Guide

```bash
# 1. Clone repository
git clone https://github.com/yourusername/Visual-Resume_Tableau-Dashboard.git
cd Visual-Resume_Tableau-Dashboard

# 2. Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configure credentials
cp .env.example .env
# Edit .env with your PostgreSQL password and Google Sheets ID (optional)

# 4. Run the pipeline
python 02_Pipeline/execute_pipeline.py

# 5. Done! Check output
ls outputs/  # visual-Resume_dashboard-data.xlsx
Then connect these Excel files to Tableau and build your dashboard or use live connection over Google Sheets (see Cloud Integration via Google Sheets).
```

---

## Project Structure

Visual-Resume_Tableau-Dashboard/
│
├── 01_Data/                          Data layer
│   ├── raw/
│   │   └── master_database.xlsx      Your resume data
│   └── schema/
│       └── ER-Diagram.md             Database schema
│
├── 02_Pipeline/                      ETL layer
│   ├── execute_pipeline.py           Main entry point
│   ├── modules/                      Database and export logic
│   ├── sql/                          Generated SQL view files
│   └── outputs/                      Excel exports
│
├── 03_Dashboard/                     Tableau workbook
├── .env.example                      Configuration template
└── requirements.txt                  Python dependencies

---

## Pipeline Overview

```
Your Data (Excel)
     └─ master_database.xlsx (17 sheets)
                │
        Python Pipeline (SQLAlchemy)
                │
    ┌───────────┴───────────┐
    │                       │
PostgreSQL          Google Sheets
17 Tables           5 Live Sheets
5 Views            Auto-Synced
    │
    └─── Excel Export
        visual-Resume_dashboard-data.xlsx
        (5 Sheets: portfolio, timeline, 
         certificates, filters, person)
                │
        ┌───────┴────────┐
        │                │
     Tableau          Python Scripts
     Dashboards       Analysis
```

---

## Cloud Integration via Google Sheets

Automatically sync your data to Google Sheets for live Tableau connections.

### Setup Steps

Create Google Cloud Project: Enable Google Sheets API
Create Service Account: Download JSON key as credentials.json
Create Google Sheet: Name it "Visual Resume Dashboard Data"
Share Sheet: Add service account email as Editor
Configure .env: Set GOOGLE_SHEETS_ID and GOOGLE_CREDENTIALS_PATH
Run Pipeline: Execute python execute_pipeline.py

---

## Common Workflow

### Update Resume & Republish

```bash
# 1. Edit data
# Open 01_Data/raw/master_database.xlsx
# Add new project, update skills, add certificate...
# Save the file

# 2. Run pipeline
cd 02_Pipeline
python execute_pipeline.py

# When prompted to overwrite files, enter 'Y'

# 3. Refresh Tableau
# (right-click data source, refresh)

# 4. Republish
# (publish to Tableau Public)
```

---

## Troubleshooting

- **DB_PASSWORD not set:** Run cp .env.example .env, edit with your password
- **Cannot connect to PostgreSQL:** Verify running: psql -U postgres
- **Excel file not found:** Check file exists: 01_Data/raw/master_database.xlsx
- **Import errors (packages):** Run: pip install -r requirements.txt --upgrade
- **Google Sheets auth failed:** Verify credentials.json exists, GOOGLE_SHEETS_ID correct
- **Foreign key violation:** IDs in join tables don't match. Verify relationships.

---

## Version Info

- **Version:** 2.0
- **Last Updated:** May 1, 2026
- **Status:** Released
- **Python:** 3.10+
- **PostgreSQL:** 12+
- **Tableau:** Public/Desktop compatible

---

## License

This project is personal portfolio work. Feel free to adapt for your own use.

---