"""
Simple test to verify the User table has the correct schema
"""
import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.session import AsyncSessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from sqlmodel import select


async def test_user_creation():
    async with AsyncSessionLocal() as session:
        # Try to query the users table to see if it has the name column
        try:
            # This will fail if the 'name' column doesn't exist
            statement = select(User.email, User.name).where(User.email == "nonexistent@example.com")
            result = await session.exec(statement)
            user = result.first()
            print("✓ Query with 'name' column succeeded - database schema is correct")
            
            # Now try to create a user with the correct password length
            from app.services.auth_service import register_user as service_register_user
            user_data = UserCreate(
                email="test@example.com",
                name="Test User",
                password="TestPass123!"  # Within bcrypt limits
            )
            
            user = await service_register_user(session, user_data)
            print(f"✓ User created successfully: {user.email}, {user.name}")
            return True
        except Exception as e:
            print(f"✗ Error: {e}")
            return False


if __name__ == "__main__":
    success = asyncio.run(test_user_creation())
    if success:
        print("✓ Database schema is correct - User table has name column")
    else:
        print("✗ Database schema issue persists")