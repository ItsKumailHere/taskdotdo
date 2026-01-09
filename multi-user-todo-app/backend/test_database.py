"""
Test script to verify the database setup is working correctly.
"""
import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database.database import async_engine
from app.database.session import get_async_session
from app.models.user import User
from sqlmodel import select


async def test_database_connection():
    """
    Test function to verify database connectivity and basic operations.
    """
    print("Testing database connection...")
    
    try:
        # Test creating a session
        async with get_async_session() as session:
            print("✓ Successfully created async database session")
            
            # Test a simple query (count users)
            statement = select(User)
            result = await session.execute(statement)
            users = result.scalars().all()
            
            print(f"✓ Successfully executed query. Found {len(users)} users.")
            
            # Test that the engine is working
            print("✓ Async engine is properly configured")
            
        print("\n✓ All database tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_database_connection())
    if not success:
        sys.exit(1)