"""
Session management for the Multi-User Todo Application.

This module provides async and sync session factories with proper
connection management and FastAPI dependency injection patterns.
"""
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator
from sqlmodel import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from .database import engine, async_engine


# Session maker for async sessions
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Session maker for sync sessions
SyncSessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for database sessions.

    Yields an async session that automatically handles commit/rollback
    and ensures proper cleanup.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            await session.close()


@contextmanager
def get_sync_session() -> Generator[Session, None, None]:
    """
    Sync context manager for database sessions.

    Yields a sync session that automatically handles commit/rollback
    and ensures proper cleanup.
    """
    with SyncSessionLocal() as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Sync database session error: {str(e)}")
            raise
        finally:
            session.close()


# FastAPI dependency functions
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an async database session.

    This function can be used as a dependency in FastAPI route handlers
    to automatically inject a database session.
    """
    async with get_async_session() as session:
        yield session