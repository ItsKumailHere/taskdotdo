"""
Migration utility functions for the Multi-User Todo Application.

This module provides utility functions to run database migrations
programmatically, which can be useful for startup scripts or testing.
"""
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine
from app.config.settings import settings
from app.database.database import engine
import os


def run_migrations_online():
    """
    Run alembic migrations in online mode.
    """
    # Create Alembic config
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    
    # Set the database URL
    alembic_cfg.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
    
    # Run the upgrade to head (latest migration)
    command.upgrade(alembic_cfg, "head")


def run_migrations_offline():
    """
    Generate migration script without connecting to database.
    """
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    alembic_cfg.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
    
    # This would be used to generate migrations without connecting to DB
    # For actual migration execution, use run_migrations_online
    pass


def generate_migration(message: str, autogenerate: bool = True):
    """
    Generate a new migration script.
    
    Args:
        message: Description of the migration
        autogenerate: Whether to autogenerate the migration from model changes
    """
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    alembic_cfg.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
    
    command.revision(alembic_cfg, message=message, autogenerate=autogenerate)


if __name__ == "__main__":
    # Run migrations when this script is executed directly
    run_migrations_online()