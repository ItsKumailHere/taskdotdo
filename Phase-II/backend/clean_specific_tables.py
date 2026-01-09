"""
Script to clean the database and recreate only our tables with correct schema
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.settings import settings
from sqlmodel import text
from app.models import Todo, User  # Import models to register them
from app.database.init_db import async_engine
from sqlmodel import SQLModel


async def clean_and_recreate():
    # Use the same engine as the app
    async with async_engine.begin() as conn:
        # Drop the todos table specifically
        await conn.execute(text("DROP TABLE IF EXISTS todos CASCADE"))
        print("Dropped todos table")
        
        # Drop the users table specifically  
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        print("Dropped users table")
        
        # Create all tables based on models
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Created all tables with correct schema")

    print("Database cleaned and recreated successfully!")


if __name__ == "__main__":
    asyncio.run(clean_and_recreate())