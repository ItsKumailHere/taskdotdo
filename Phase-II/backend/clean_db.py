"""
Script to clean the database and recreate only our tables
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.settings import settings
from sqlmodel import text


async def clean_and_recreate():
    engine = create_async_engine(settings.DATABASE_URL)
    
    async with engine.begin() as conn:
        # Drop specific tables that are not from our models
        tables_to_drop = ['User', 'Post', 'tags', 'categories', 'sessions', 'todo_tags', 'notifications', '_prisma_migrations']
        
        for table in tables_to_drop:
            try:
                await conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
                print(f"Dropped table: {table}")
            except Exception as e:
                print(f"Error dropping table {table}: {e}")
        
        # Also drop the users table to recreate it properly
        await conn.execute(text('DROP TABLE IF EXISTS "users" CASCADE'))
        print("Dropped table: users")
    
    # Now recreate only our tables
    from app.models import user, todo  # Import models to register them
    from app.models.user import User
    from app.models.todo import Todo
    from sqlmodel import SQLModel
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Created our tables")
    
    await engine.dispose()
    print("Database cleaned and reset successfully!")


if __name__ == "__main__":
    asyncio.run(clean_and_recreate())