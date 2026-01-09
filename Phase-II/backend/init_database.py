"""
Script to initialize the database with the correct schema
"""
import asyncio
import os
from app.database.init_db import init_db
from app.config.settings import settings


async def main():
    # Set the DATABASE_URL environment variable from settings if not already set
    if not os.getenv("DATABASE_URL"):
        os.environ["DATABASE_URL"] = settings.DATABASE_URL
    
    print("Initializing database...")
    await init_db()
    print("Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(main())