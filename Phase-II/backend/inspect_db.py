"""
Script to inspect the database tables and their structure
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.settings import settings
from sqlmodel import text


async def inspect_db():
    engine = create_async_engine(settings.DATABASE_URL)
    
    async with engine.begin() as conn:
        # Get all table names
        result = await conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """))
        tables = result.fetchall()
        print("Tables in database:")
        for table in tables:
            print(f"  - {table[0]}")

        # Check columns in the users table if it exists
        if ('users',) in tables:
            result = await conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'users'
                ORDER BY ordinal_position
            """))
            columns = result.fetchall()
            print(f"\nColumns in 'users' table:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")

        # Check columns in the todos table if it exists
        if ('todos',) in tables:
            result = await conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'todos'
                ORDER BY ordinal_position
            """))
            columns = result.fetchall()
            print(f"\nColumns in 'todos' table:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(inspect_db())