# Visual Resume Dashboard

Interactive Tableau dashboard presenting professional expertise, career timeline, skills, and portfolio projects. Data-driven alternative to traditional resumes.

**View Dashboard:** [Tableau Public Link](https://public.tableau.com/app/profile/cedric.hering.peter/viz/CV-Dashboard_17551211549430/Published_Apr-26?publish=yes)

---

## Overview

Personal dashboard built to showcase:
- Career timeline and professional milestones
- Technical skills and language proficiencies  
- Project portfolio with technologies used
- Educational certificates and continuous learning
- Interactive filtering by thematic domains (Data Scientist, Biologist, Consultant)

**Tech Stack:** PostgreSQL → Python/Excel → Tableau Public

---

## Project Structure

```
Visual-Resume_Tableau-Dashboard/
├── README.md                   This file
├── requirements.txt            Python dependencies
├── 01_ER-Diagram/              Database schema documentation
├── 02_Database/                Master database files
├── 03_Scripts/                 Data pipeline (Python + SQL)
│   ├── 01_Python/              ETL scripts
│   ├── 02_SQL/                 Database views
│   └── 03_Exports/             Generated Excel exports
└── 04_Media/                   Dashboard design assets
```

---

## Getting Started (Local Setup & Deployment)

### Prerequisites
- PostgreSQL 12+
- Python 3.10+
- Tableau Desktop or public version

### Setup

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or .venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python 03_Scripts/01_Python/2025-08-12_Schema-Setup.py

# 4. Run data pipeline
python 03_Scripts/01_Python/2025-08-28_Create-and-Export-Views.py

# 5. Open Tableau
# Connect to Excel files in 03_Scripts/03_Exports/
```

### Deployment
1. Export Excel files from ETL pipeline
2. Upload to Tableau Public
3. Connect dashboard worksheets to exported Excel files
4. Design dashboard with visual hierarchy and filters
5. Publish to public URL

---

## How It Works

1. **Data Source:** PostgreSQL master database with normalized schema
2. **Views:** SQL views flatten data into analytical format
3. **Export:** Python script executes views and exports to Excel
4. **Visualization:** Tableau connects to Excel for interactive dashboard
5. **Publishing:** Dashboard published to Tableau Public

See `01_ER-Diagram/` for database schema and relationships.

### Data Entry Workflow
1. Update master database: `02_Database/2025-09-05_Database.xlsx`
2. Run ETL pipeline: Creates normalized views and exports
3. Refresh data in Tableau Public
4. Verify dashboard updates

---

## Key Resources

- **Tableau Public Dashboard**: [Visual Resume Dashboard](https://public.tableau.com/)
- **ER Diagram**: See [01_ER-Diagram/](01_ER-Diagram/) for database schema visualization
- **Product Requirements**: See [PRD.md](PRD.md) for original vision and iteration history

---

### Version History
- **v1.0** (2025-10-01) - Initial release with core views (Timeline, Skills, Portfolio)
- **v1.1** (2026-04-15) - Updated Certificates, Timeline and Domain Descriptions
- Planned: v1.2 - Streamlit PhD Data Project

---

## Author

**Dr. Cedric Hering-Peter** - Computational Sustainability Scientist  
*Bridging biotechnology, data science, and strategy for sustainable innovation*

---

## License

This project is part of a personal portfolio and branding initiative. Database schema and visualizations are original work. Design assets and content are proprietary.

---

*Last Updated: 2026-04-14*
