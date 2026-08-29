from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_URL = "sqlite:///./quantum_learning.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


# ============================================================
# DATABASE SESSION
# ============================================================

def get_db():
    """
    Provide a database session for FastAPI requests.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

def create_database_tables():
    """
    Create all SQLAlchemy tables that do not already exist.
    """

    # Import models so SQLAlchemy registers them with Base.
    from app.db import models

    Base.metadata.create_all(
        bind=engine
    )