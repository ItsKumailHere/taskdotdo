"""
Database engine configuration for the Multi-User Todo Application.

This module sets up both sync and async engines with proper configuration
for Neon PostgreSQL, including connection pooling and async support.
"""
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from app.config.settings import settings
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Synchronous database engine for sync operations
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Set to True to see SQL queries in logs
    pool_pre_ping=True,   # Verify connections before use
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,  # Recycle connections after 5 minutes
    pool_timeout=30,
    connect_args={
        "connect_timeout": 10,
    }
)

# Async database engine for async operations
# Replace postgresql:// with postgresql+asyncpg:// for async support
async_database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
async_engine: AsyncEngine = create_async_engine(
    async_database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,  # Recycle connections after 5 minutes
    pool_timeout=30,
    connect_args={
        "server_settings": {
            "application_name": "multi-user-todo-app",
        },
        "timeout": 10,
    }
)

logger.info("Database engines initialized successfully")