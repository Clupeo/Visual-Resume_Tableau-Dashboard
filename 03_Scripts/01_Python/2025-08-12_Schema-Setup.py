import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base

# -----------------
# CONFIG
# -----------------
db_user = "postgres"
db_password = "#01805#SQL#"
db_host = "localhost"
db_port = "5432"
db_name = "Dashboard_Resume"

# -----------------
# Path to Excel file
# -----------------
excel_file = "../02_Database/2025-09-05_Database.xlsx"

# -----------------
# ORM MODEL
# -----------------
Base = declarative_base()

class Person(Base):
    __tablename__ = "person"
    person_id = Column(Integer, primary_key=True)
    title = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    location = Column(String)
    profile_description = Column(String)
    birth_date = Column(Date)
    career_goal = Column(String)
    
class Domain(Base):
    __tablename__ = "domain"
    domain_id = Column(Integer, primary_key=True)
    domain = Column(String)
    description = Column(String)
    hashtags = Column(String)
    
class Activity(Base):
    __tablename__ = "activity"
    activity_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    title = Column(String)
    organization = Column(String)
    location = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)
    hashtags = Column(String)

class ActivityDomain(Base):
    __tablename__ = "activity_domain"
    activity_id = Column(Integer, ForeignKey("activity.activity_id"), primary_key=True)
    domain_id = Column(Integer, ForeignKey("domain.domain_id"), primary_key=True)

class Certificates(Base):
    __tablename__ = "certificates"
    certificate_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    name = Column(String)
    place = Column(String)
    category = Column(String)
    image = Column(String)

class CertificatesDomain(Base):
    __tablename__ = "certificates_domain"
    certificate_id = Column(Integer, ForeignKey("certificates.certificate_id"), primary_key=True)
    domain_id = Column(Integer, ForeignKey("domain.domain_id"), primary_key=True)

class Portfolio(Base):
    __tablename__ = "portfolio"
    portfolio_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    project_name = Column(String)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String)
    link = Column(String)
    
class PortfolioDomain(Base):
    __tablename__ = "portfolio_domain"
    portfolio_id = Column(Integer, ForeignKey("portfolio.portfolio_id"), primary_key=True)
    domain_id = Column(Integer, ForeignKey("domain.domain_id"), primary_key=True)

class Skills(Base):
    __tablename__ = "skills"
    skill_id = Column(Integer, primary_key=True)
    skill_name = Column(String)
    category = Column(String)
    description = Column(String)

class PersonSkills(Base):
    __tablename__ = "person_skills"
    person_id = Column(Integer, ForeignKey("person.person_id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), primary_key=True)
    proficiency_level = Column(Integer)

class Tools(Base):
    __tablename__ = "tools"
    tool_id = Column(Integer, primary_key=True)
    tool_name = Column(String)
    category = Column(String)
    description = Column(String)

class PersonTools(Base):
    __tablename__ = "person_tools"
    person_id = Column(Integer, ForeignKey("person.person_id"), primary_key=True)
    tool_id = Column(Integer, ForeignKey("tools.tool_id"), primary_key=True)
    proficiency_level = Column(Integer)

class PortfolioSkills(Base):
    __tablename__ = "portfolio_skills"
    portfolio_id = Column(Integer, ForeignKey("portfolio.portfolio_id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), primary_key=True)

class PortfolioTools(Base):
    __tablename__ = "portfolio_tools"
    portfolio_id = Column(Integer, ForeignKey("portfolio.portfolio_id"), primary_key=True)
    tool_id = Column(Integer, ForeignKey("tools.tool_id"), primary_key=True)

class Languages(Base):
    __tablename__ = "languages"
    language_id = Column(Integer, primary_key=True)
    language_name = Column(String)

class PersonLanguages(Base):
    __tablename__ = "person_languages"
    person_id = Column(Integer, ForeignKey("person.person_id"), primary_key=True)
    language_id = Column(Integer, ForeignKey("languages.language_id"), primary_key=True)
    proficiency_id = Column(Integer, ForeignKey("languages_proficiency.proficiency_id"), primary_key=True)

class ProficiencyLanguages(Base):
    __tablename__ = "languages_proficiency"
    proficiency_id = Column(Integer, primary_key=True)
    proficiency_name = Column(String)

# -----------------
# DB CONNECTION
# -----------------
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# -----------------
# CREATE TABLES IF NOT EXISTS
# -----------------
Base.metadata.create_all(engine)
print("✅ Tables created (if not existing).")

# -----------------
# DELETE all tables
# -----------------
with engine.connect() as conn:
    print("🗑 Deleting ALL tables in database...")
    conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
    conn.commit()
    
# -----------------
# IMPORT FROM EXCEL (in dependency order)
# -----------------

sheet_to_table_ordered = [ # Ordered list for insert
    "person",
    "domain",
    "activity",
    "activity_domain",
    "certificates",
    "certificates_domain", 
    "portfolio",
    "portfolio_domain",
    "skills",
    "person_skills", 
    "portfolio_skills", 
    "tools",
    "person_tools", 
    "portfolio_tools", 
    "languages", 
    "languages_proficiency",
    "person_languages",
]

for sheetname in sheet_to_table_ordered:
    print(f"⬆ Uploading excel sheet '{sheetname}' → sql table '{sheetname}'")
    df = pd.read_excel(excel_file, sheet_name=sheetname)
    df = df.where(pd.notnull(df), None)
    df.to_sql(sheetname, engine, if_exists="append", index=False)

print("✅ All data loaded successfully.")