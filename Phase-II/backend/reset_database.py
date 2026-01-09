"""
Script to reset the database with the correct schema
"""
import asyncio
import os
from sqlmodel import SQLModel, text
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.settings import settings


async def reset_db():
    # Create an engine to execute raw SQL
    engine = create_async_engine(settings.DATABASE_URL)
    
    async with engine.begin() as conn:
        # First, let's try to drop all tables individually
        # Get all table names from metadata
        table_names = [table.name for table in SQLModel.metadata.sorted_tables]
        
        # Drop tables in reverse order to handle foreign key dependencies
        for table in reversed(SQLModel.metadata.sorted_tables):
            try:
                await conn.execute(text(f"DROP TABLE IF EXISTS {table.name} CASCADE"))
                print(f"Dropped table: {table.name}")
            except Exception as e:
                print(f"Error dropping table {table.name}: {e}")
        
        # Create all tables based on models
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Created all tables")
    
    await engine.dispose()
    print("Database reset successfully!")


if __name__ == "__main__":
    asyncio.run(reset_db())