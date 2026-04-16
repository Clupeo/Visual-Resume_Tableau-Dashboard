# Entity-Relationship Diagram (ERD)
## Visual Resume Dashboard Database Schema

---

## Overview

The database uses a **normalized 3NF schema** with 17 tables organized into:
- **Core Entities** (5): Person, Activity, Portfolio, Certificate, Skill, Tool
- **Reference Tables** (2): Domain
- **Junction Tables** (10): Many-to-many relationships

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CORE ENTITIES                             │
└─────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │    PERSON    │
                              │──────────────│
                              │ person_id PK │
                              │ title        │
                              │ first_name   │
                              │ last_name    │
                              │ location     │
                              │ profile_desc │
                              │ birth_date   │
                              │ career_goal  │
                              └──────┬───────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
    ┌──────────────────┐  ┌─────────────────┐  ┌──────────────────┐
    │    ACTIVITY      │  │   PORTFOLIO     │  │   CERTIFICATE    │
    │──────────────────│  │─────────────────│  │──────────────────│
    │ activity_id PK   │  │ portfolio_id PK │  │certificate_id PK │
    │ person_id FK     │  │ person_id FK    │  │ person_id FK     │
    │ title            │  │ project_name    │  │ name             │
    │ organization     │  │ description     │  │ place            │
    │ location         │  │ start_date      │  │ category         │
    │ start_date       │  │ end_date        │  │ image            │
    │ end_date         │  │ status          │  └──────────────────┘
    │ description      │  │ link            │
    │ hashtags         │  └─────────────────┘
    └──────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                    REFERENCE/LOOKUP TABLES                       │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐   
                    │     DOMAIN       │  
                    │──────────────────│   
                    │ domain_id PK     │  
                    │ domain           │    
                    │ description      │   
                    │ hashtags         │    
                    └──────────┬───────┘
                               │
    ┌────────────────────────────────────────────────────┐
    │            SKILLS & TOOLS                          │
    ├────────────────────────────────────────────────────┤
    │  ┌──────────────────┐    ┌──────────────────┐     │
    │  │     SKILLS       │    │      TOOLS       │     │
    │  │──────────────────│    │──────────────────│     │
    │  │ skill_id PK      │    │ tool_id PK       │     │
    │  │ skill_name       │    │ tool_name        │     │
    │  │ category         │    │ category         │     │
    │  │ description      │    │ description      │     │
    │  └──────────────────┘    └──────────────────┘     │
    └────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  JUNCTION (MANY-TO-MANY) TABLES                  │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────┐
    │   ACTIVITY_DOMAIN        │ ← Activity classified by domains
    │──────────────────────────│
    │ activity_id FK (PK)      │
    │ domain_id FK (PK)        │
    └──────────────────────────┘

    ┌──────────────────────────┐
    │   PORTFOLIO_DOMAIN       │ ← Projects classified by domains
    │──────────────────────────│
    │ portfolio_id FK (PK)     │
    │ domain_id FK (PK)        │
    └──────────────────────────┘

    ┌──────────────────────────┐
    │   CERTIFICATES_DOMAIN    │ ← Certs classified by domains
    │──────────────────────────│
    │ certificate_id FK (PK)   │
    │ domain_id FK (PK)        │
    └──────────────────────────┘

    ┌──────────────────────────┐
    │   PERSON_SKILLS          │ ← Person's skills + proficiency
    │──────────────────────────│
    │ person_id FK (PK)        │
    │ skill_id FK (PK)         │
    │ proficiency_level        │
    └──────────────────────────┘

    ┌──────────────────────────┐
    │   PERSON_TOOLS           │ ← Person's tools + proficiency
    │──────────────────────────│
    │ person_id FK (PK)        │
    │ tool_id FK (PK)          │
    │ proficiency_level        │
    └──────────────────────────┘

    ┌──────────────────────────┐
    │   PORTFOLIO_SKILLS       │ ← Skills used in projects
    │──────────────────────────│
    │ portfolio_id FK (PK)     │
    │ skill_id FK (PK)         │
    └──────────────────────────┘

    ┌──────────────────────────┐
    │   PORTFOLIO_TOOLS        │ ← Tools used in projects
    │──────────────────────────│
    │ portfolio_id FK (PK)     │
    │ tool_id FK (PK)          │
    └──────────────────────────┘
    
```

---

## Table Definitions

### Core Tables

#### PERSON
**Purpose:** Core professional profile information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| person_id | INTEGER | PRIMARY KEY | Unique person identifier |
| title | VARCHAR | - | Professional title (e.g., "Dr.") |
| first_name | VARCHAR | - | First name |
| last_name | VARCHAR | - | Last name |
| location | VARCHAR | - | Current location |
| profile_description | TEXT | - | Professional summary |
| birth_date | DATE | - | Date of birth |
| career_goal | VARCHAR | - | Career objective/goal |

**Primary Key:** person_id

---

#### ACTIVITY
**Purpose:** Professional experiences (jobs, projects, consulting)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| activity_id | INTEGER | PRIMARY KEY | Unique activity identifier |
| person_id | INTEGER | FOREIGN KEY → person | Reference to person |
| title | VARCHAR | - | Job title / position |
| organization | VARCHAR | - | Organization / company name |
| location | VARCHAR | - | Work location |
| start_date | DATE | - | Start date |
| end_date | DATE | - | End date (NULL if current) |
| description | TEXT | - | Details about the role |
| hashtags | VARCHAR | - | Comma-separated tags |

**Primary Key:** activity_id  
**Foreign Key:** person_id → person.person_id

---

#### PORTFOLIO
**Purpose:** Professional projects and portfolio items

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| portfolio_id | INTEGER | PRIMARY KEY | Unique project identifier |
| person_id | INTEGER | FOREIGN KEY → person | Reference to person |
| project_name | VARCHAR | - | Project title |
| description | TEXT | - | Project description |
| start_date | DATE | - | Project start date |
| end_date | DATE | - | Project end date |
| status | VARCHAR | - | Current status (active, completed, etc) |
| link | VARCHAR | - | URL to project / demo / repo |

**Primary Key:** portfolio_id  
**Foreign Key:** person_id → person.person_id

---

#### CERTIFICATE
**Purpose:** Educational certificates and credentials

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| certificate_id | INTEGER | PRIMARY KEY | Unique certificate identifier |
| person_id | INTEGER | FOREIGN KEY → person | Reference to person |
| name | VARCHAR | - | Certificate / diploma name |
| place | VARCHAR | - | Issuing organization |
| category | VARCHAR | - | Type (degree, certification, etc) |
| image | VARCHAR | - | URL to certificate image |

**Primary Key:** certificate_id  
**Foreign Key:** person_id → person.person_id

---

### Reference Tables

#### DOMAIN
**Purpose:** Professional domains for classification (Data Scientist, Biologist, etc.)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| domain_id | INTEGER | PRIMARY KEY | Unique domain identifier |
| domain | VARCHAR | UNIQUE | Domain name |
| description | TEXT | - | Domain description |
| hashtags | VARCHAR | - | Associated hashtags |

**Primary Key:** domain_id

---

#### SKILLS
**Purpose:** Skill library (technical, soft, domain-specific)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| skill_id | INTEGER | PRIMARY KEY | Unique skill identifier |
| skill_name | VARCHAR | - | Skill name |
| category | VARCHAR | - | Skill category |
| description | TEXT | - | Skill description |

**Primary Key:** skill_id

---

#### TOOLS
**Purpose:** Software tools and technologies

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| tool_id | INTEGER | PRIMARY KEY | Unique tool identifier |
| tool_name | VARCHAR | - | Tool/software name |
| category | VARCHAR | - | Category (Programming, BI, Database, etc) |
| description | TEXT | - | Tool description |

**Primary Key:** tool_id

---

### Junction Tables

#### ACTIVITY_DOMAIN (Many-to-Many)
**Purpose:** Associate activities with domains

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| activity_id | INTEGER | FOREIGN KEY → activity (PK) | Activity reference |
| domain_id | INTEGER | FOREIGN KEY → domain (PK) | Domain reference |

**Primary Key:** (activity_id, domain_id)

---

#### PORTFOLIO_DOMAIN (Many-to-Many)
**Purpose:** Associate projects with domains

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| portfolio_id | INTEGER | FOREIGN KEY → portfolio (PK) | Project reference |
| domain_id | INTEGER | FOREIGN KEY → domain (PK) | Domain reference |

**Primary Key:** (portfolio_id, domain_id)

---

#### CERTIFICATES_DOMAIN (Many-to-Many)
**Purpose:** Associate certificates with domains

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| certificate_id | INTEGER | FOREIGN KEY → certificate (PK) | Certificate reference |
| domain_id | INTEGER | FOREIGN KEY → domain (PK) | Domain reference |

**Primary Key:** (certificate_id, domain_id)

---

#### PERSON_SKILLS (Many-to-Many with Proficiency)
**Purpose:** Skills with proficiency levels

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| person_id | INTEGER | FOREIGN KEY → person (PK) | Person reference |
| skill_id | INTEGER | FOREIGN KEY → skills (PK) | Skill reference |
| proficiency_level | INTEGER | - | Proficiency 1-5 (1=Beginner, 5=Expert) |

**Primary Key:** (person_id, skill_id)

---

#### PERSON_TOOLS (Many-to-Many with Proficiency)
**Purpose:** Tools with proficiency levels

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| person_id | INTEGER | FOREIGN KEY → person (PK) | Person reference |
| tool_id | INTEGER | FOREIGN KEY → tools (PK) | Tool reference |
| proficiency_level | INTEGER | - | Proficiency 1-5 (1=Beginner, 5=Expert) |

**Primary Key:** (person_id, tool_id)

---

#### PORTFOLIO_SKILLS (Many-to-Many)
**Purpose:** Skills used in projects

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| portfolio_id | INTEGER | FOREIGN KEY → portfolio (PK) | Project reference |
| skill_id | INTEGER | FOREIGN KEY → skills (PK) | Skill reference |

**Primary Key:** (portfolio_id, skill_id)

---

#### PORTFOLIO_TOOLS (Many-to-Many)
**Purpose:** Tools used in projects

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| portfolio_id | INTEGER | FOREIGN KEY → portfolio (PK) | Project reference |
| tool_id | INTEGER | FOREIGN KEY → tools (PK) | Tool reference |

**Primary Key:** (portfolio_id, tool_id)

---

**Last Updated:** April 15, 2025  
**Schema Version:** 1.0  