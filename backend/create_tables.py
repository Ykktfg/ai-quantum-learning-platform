from app.db.database import engine, Base
from app.db.models import (
    User,
    Course,
    Enrollment,
    Progress,
)


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

def create_tables():
    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()