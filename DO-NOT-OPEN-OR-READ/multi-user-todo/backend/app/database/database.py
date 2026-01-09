"""Database connection setup and initialization for Neon PostgreSQL."""

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from app.config.settings import settings

# Process database URL for asyncpg SSL requirements
def get_database_url() -> str:
    """
    Process database URL to handle SSL configuration for asyncpg.

    Neon requires SSL, but asyncpg doesn't accept 'sslmode' as a query parameter.
    Instead, we need to use connect_args with ssl parameter.
    """
    url = settings.database_url
    # Remove sslmode from URL if present (asyncpg doesn't support it in URL)
    if "?sslmode=" in url or "&sslmode=" in url:
        url = url.split("?sslmode=")[0].split("&sslmode=")[0]
    return url


# Create async engine with Neon-optimized settings
engine = create_async_engine(
    get_database_url(),
    echo=settings.debug,  # SQL logging in debug mode
    future=True,
    pool_pre_ping=True,  # Verify connections before using (important for Neon)
    pool_size=5,  # Limit connection pool for serverless
    max_overflow=10,  # Additional connections when pool is full
    connect_args={
        "ssl": "require",  # SSL mode for asyncpg (required for Neon)
        "server_settings": {
            "application_name": "multi-user-todo",
        },
    },
)


async def init_db() -> None:
    """
    Initialize database by creating all tables.

    This should be called once when the application starts.
    For production, consider using Alembic migrations instead.
    """
    async with engine.begin() as conn:
        # Import all models to ensure they are registered
        # This must be done before create_all()
        from app.models import (  # noqa: F401
            user,
            todo,
            tag,
            category,
            todo_tag,
            notification,
            session,
        )

        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_db() -> None:
    """
    Drop all tables from the database.

    WARNING: This will delete all data! Use only in development/testing.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
