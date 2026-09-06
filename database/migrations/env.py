from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ------------------------------------------------------------
# Make project root importable
# ------------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

BACKEND_ROOT = os.path.join(PROJECT_ROOT, "backend")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

# ------------------------------------------------------------
# Import SQLAlchemy Base and models
# ------------------------------------------------------------

from app.db.database import Base
from app.db import models

# ------------------------------------------------------------
# Alembic Config
# ------------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ------------------------------------------------------------
# Metadata for autogenerate
# ------------------------------------------------------------

target_metadata = Base.metadata


# ------------------------------------------------------------
# Offline migrations
# ------------------------------------------------------------

def run_migrations_offline() -> None:
    """Run migrations without creating a database connection."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ------------------------------------------------------------
# Online migrations
# ------------------------------------------------------------

def run_migrations_online() -> None:
    """Run migrations using a live database connection."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ------------------------------------------------------------
# Run
# ------------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()