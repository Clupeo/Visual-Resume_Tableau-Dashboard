"""
Database Module for Visual Resume Dashboard
===========================================

Handles all database connections, ORM models, and schema management.

Design Principles:
- Single responsibility: database operations only
- Type hints for clarity
- Comprehensive docstrings
- Error handling with logging
"""

import logging
from typing import Optional
from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    String, 
    Date, 
    Boolean, 
    ForeignKey, 
    text,
    Engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


# ==========================================
# ORM MODELS (Database Schema Definition)
# ==========================================

class Person(Base):
    """Person table: Core profile information."""
    __tablename__ = "person"
    person_id = Column(Integer, primary_key=True)
    title = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    city = Column(String)
    province = Column(String)
    country = Column(String)
    birth_date = Column(Date)


class Domain(Base):
    """Domain table: Thematic domains (Data Scientist, Biologist, etc.)."""
    __tablename__ = "domain"
    domain_id = Column(Integer, primary_key=True)
    name = Column(String)
    subtitle = Column(String)
    description = Column(String)
    hashtags = Column(String)


class Activity(Base):
    """Activity table: Professional experiences (jobs, projects, etc.)."""
    __tablename__ = "activity"
    activity_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    title = Column(String)
    organization = Column(String)
    location = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)


class ActivityDomain(Base):
    """Junction table: Links activities to domains (many-to-many)."""
    __tablename__ = "activity_domain"
    activity_id = Column(Integer, ForeignKey("activity.activity_id"), primary_key=True)
    domain_id = Column(Integer, ForeignKey("domain.domain_id"), primary_key=True)


class Certificate(Base):
    """Certificate table: Educational certificates and credentials."""
    __tablename__ = "certificates"
    certificate_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    name = Column(String)
    place = Column(String)
    issue_date = Column(Date)
    image = Column(String)


class CertificateDomain(Base):
    """Junction table: Links certificates to domains (many-to-many)."""
    __tablename__ = "certificates_domain"
    certificate_id = Column(Integer, ForeignKey("certificates.certificate_id"), primary_key=True)
    domain_id = Column(Integer, ForeignKey("domain.domain_id"), primary_key=True)


class Portfolio(Base):
    """Portfolio table: Professional projects and portfolio items."""
    __tablename__ = "portfolio"
    portfolio_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    title = Column(String)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String)
    link = Column(String)


class PortfolioDomain(Base):
    """Junction table: Links portfolio items to domains (many-to-many)."""
    __tablename__ = "portfolio_domain"
    portfolio_id = Column(Integer, ForeignKey("portfolio.portfolio_id"), primary_key=True)
    domain_id = Column(Integer, ForeignKey("domain.domain_id"), primary_key=True)


class Skill(Base):
    """Skill table: Professional skills (programming, data analysis, etc.)."""
    __tablename__ = "skills"
    skill_id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    proficiency_level = Column(Integer)
    description = Column(String)
    project_occurance = Column("project occurance", String)  # Space in column name from Excel


class PersonSkill(Base):
    """Junction table: Links person to skills (proficiency now in skills table)."""
    __tablename__ = "person_skills"
    person_id = Column(Integer, ForeignKey("person.person_id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), primary_key=True)


class Tool(Base):
    """Tool table: Software tools and technologies (Python, SQL, Tableau, etc.)."""
    __tablename__ = "tools"
    tool_id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    description = Column(String)
    proficiency_level = Column(Integer)
    project_occurance = Column("project occurance", String)  # Space in column name from Excel


class PersonTool(Base):
    """Junction table: Links person to tools (proficiency now in tools table)."""
    __tablename__ = "person_tools"
    person_id = Column(Integer, ForeignKey("person.person_id"), primary_key=True)
    tool_id = Column(Integer, ForeignKey("tools.tool_id"), primary_key=True)


class PortfolioSkill(Base):
    """Junction table: Links portfolio items to skills used (many-to-many)."""
    __tablename__ = "portfolio_skills"
    portfolio_id = Column(Integer, ForeignKey("portfolio.portfolio_id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), primary_key=True)


class PortfolioTool(Base):
    """Junction table: Links portfolio items to tools used (many-to-many)."""
    __tablename__ = "portfolio_tools"
    portfolio_id = Column(Integer, ForeignKey("portfolio.portfolio_id"), primary_key=True)
    tool_id = Column(Integer, ForeignKey("tools.tool_id"), primary_key=True)


# ==========================================
# DATABASE CONNECTION MANAGEMENT
# ==========================================

class DatabaseManager:
    """
    Centralized database management class.
    Handles connections, session management, and schema operations.
    """
    
    _engine: Optional[Engine] = None
    _SessionLocal = None
    
    @classmethod
    def get_engine(cls) -> Engine:
        """
        Get or create database engine.
        
        Returns:
            Engine: SQLAlchemy database engine
        """
        if cls._engine is None:
            db_url = Config.get_database_url()
            cls._engine = create_engine(db_url, echo=False)
            logger.info(f"✅ Database engine created: {Config.DB_NAME}")
        return cls._engine
    
    @classmethod
    def get_session_factory(cls):
        """Get SQLAlchemy session factory."""
        if cls._SessionLocal is None:
            cls._SessionLocal = sessionmaker(bind=cls.get_engine())
        return cls._SessionLocal
    
    @classmethod
    def create_session(cls) -> Session:
        """Create a new database session."""
        SessionLocal = cls.get_session_factory()
        return SessionLocal()
    
    @classmethod
    def create_all_tables(cls) -> None:
        """Create all tables if they don't exist."""
        engine = cls.get_engine()
        Base.metadata.create_all(engine)
        logger.info("✅ All tables created (or already exist)")
    
    @classmethod
    def drop_all_tables(cls) -> None:
        """
        Drop all tables and recreate schema (for data refresh).
        WARNING: This deletes all data!
        """
        engine = cls.get_engine()
        with engine.connect() as conn:
            logger.warning("🗑  Dropping ALL tables (this deletes all data)...")
            conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
            conn.commit()
            logger.info("✅ Schema recreated")
    
    @classmethod
    def execute_sql(cls, sql_query: str) -> None:
        """
        Execute a raw SQL query.
        
        Args:
            sql_query: SQL query as string
        """
        engine = cls.get_engine()
        with engine.connect() as conn:
            try:
                conn.execute(text(sql_query))
                conn.commit()
                logger.info("✅ SQL query executed")
            except Exception as e:
                logger.error(f"❌ SQL execution error: {e}")
                conn.rollback()
                raise
    
    @classmethod
    def get_view_as_dataframe(cls, view_name: str):
        """
        Query a SQL view and return results as pandas DataFrame.
        
        Args:
            view_name: Name of the SQL view to query
            
        Returns:
            pandas.DataFrame: Query results
        """
        import pandas as pd
        
        engine = cls.get_engine()
        try:
            query = f"SELECT * FROM {view_name};"
            df = pd.read_sql_query(query, engine)
            logger.info(f"✅ Loaded {len(df)} rows from {view_name}")
            return df
        except Exception as e:
            logger.error(f"❌ Failed to load {view_name}: {e}")
            raise


if __name__ == "__main__":
    # Test database connection
    db = DatabaseManager()
    engine = db.get_engine()
    print(f"✅ Database connection test: {Config.DB_NAME}")
