"""
Database initialization module
"""
from .session import async_engine
from sqlmodel import SQLModel


async def init_db():
    """
    Initialize the database by creating all tables
    """
    async with async_engine.begin() as conn:
        # Create all tables defined in SQLModel models
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db():
    """
    Close the database engine
    """
    await async_engine.dispose()