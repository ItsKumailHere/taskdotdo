"""
Simple test to verify the User table has the correct schema
"""
import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.session import AsyncSessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth_service import register_user as service_register_user
from app.models.user import get_password_hash
from sqlmodel import select


async def test_user_creation():
    async with AsyncSessionLocal() as session:
        # Try to create a test user
        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            password="Test123!"
        )
        
        try:
            user = await service_register_user(session, user_data)
            print(f"User created successfully: {user.email}, {user.name}")
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False


if __name__ == "__main__":
    success = asyncio.run(test_user_creation())
    if success:
        print("✓ Database schema is correct - User table has name column")
    else:
        print("✗ Database schema issue persists")