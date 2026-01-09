"""Async session management for database operations."""

from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.database import engine

# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevents lazy loading issues after commit
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI endpoints to get database session.

    Usage:
        @app.get("/items")
        async def get_items(session: AsyncSession = Depends(get_session)):
            statement = select(Item)
            result = await session.exec(statement)
            return result.all()

    The session is automatically closed after the request completes.
    """
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
