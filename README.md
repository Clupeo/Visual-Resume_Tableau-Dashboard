# Visual Résumé - Tableau Dashboard

Interactive Tableau dashboard showcasing professional expertise, career timeline, skills, and portfolio projects. A data-driven alternative to traditional resumes.

**Live Dashboard:** [Tableau Public](https://public.tableau.com/app/profile/cedric.hering.peter/viz/CV-Dashboard_17551211549430/Published_Apr-26?publish=yes)

---

## What Is This?

A complete system for maintaining a resume/portfolio as a database and visualizing it as an interactive dashboard:

- **Data Source:** Excel spreadsheet with your professional data
- **Database:** PostgreSQL stores normalized data with relationships
- **Pipeline:** Python script imports, processes, and exports
- **Dashboard:** Tableau visualizes the data interactively
- **Publish:** Share publicly via Tableau Public

**Tech Stack:** Excel → PostgreSQL → Python → Excel → Tableau

---

## What It Does

The pipeline (`execute_pipeline.py`) in one command:

1. Creates PostgreSQL database schema (17 tables)
2. Imports data from Excel master file
3. Generates 4 analytical views
4. Saves SQL files to `sql/` folder
5. Exports to Excel files (Tableau-ready)

**Result:** 4 Excel files ready for Tableau:
- `portfolio_view.xlsx` - Your projects with skills/tools
- `timeline_view.xlsx` - Career timeline and activities
- `certificate_view.xlsx` - Education and certifications
- `filter_view.xlsx` - Domain reference data

---

## Quick Start Guide

Get up and running in 5 minutes:

```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the pipeline
cd 02_Pipeline
python execute_pipeline.py

# 4. Done! Check output
ls outputs/  # portfolio_view.xlsx, timeline_view.xlsx, etc.
```

Then connect these Excel files to Tableau and build your dashboard.

---

## Prerequisites

Before you start, ensure you have:

- **PostgreSQL 12+** - Download from [postgresql.org](https://www.postgresql.org/)
- **Python 3.10+** - Download from [python.org](https://www.python.org/)
- **Tableau Desktop or Public account** - Get from [tableau.com](https://www.tableau.com/)

Verify installations:
```bash
psql --version          # PostgreSQL
python --version        # Python
```

---

## Common Workflows

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

## Version Info

- **Version:** 1.0
- **Last Updated:** April 15, 2026
- **Status:** Released
- **Python:** 3.10+
- **PostgreSQL:** 12+
- **Tableau:** Public/Desktop compatible

---

## License

This project is personal portfolio work. Feel free to adapt for your own use.

---

