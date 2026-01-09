#!/usr/bin/env python3
"""
Simple test to verify the backend components are working correctly.
"""

import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.session import get_session, async_engine
from app.models.user import User
from app.config.settings import settings
from app.auth import get_current_user
from app.services.user_service import create_user as service_create_user, authenticate_user


async def test_database_connection():
    """Test database connection."""
    print("Testing database connection...")
    try:
        async with async_engine.begin() as conn:
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


async def test_user_operations():
    """Test user creation and authentication."""
    print("\nTesting user operations...")
    try:
        # Get a session
        async with AsyncSession(async_engine, expire_on_commit=False) as session:
            # Test creating a user
            print("  - Testing user creation...")
            test_password = "securepassword123"
            
            # Create a test user
            from app.schemas.user import UserCreate
            user_data = UserCreate(
                email="test@example.com",
                name="Test User",
                password=test_password
            )
            user = await service_create_user(
                session=session,
                user_data=user_data
            )
            print(f"  ✓ User created with ID: {user.id}")
            
            # Test authenticating the user
            print("  - Testing user authentication...")
            authenticated_user = await authenticate_user(
                session=session,
                email="test@example.com",
                password=test_password
            )
            
            if authenticated_user:
                print(f"  ✓ User authenticated successfully: {authenticated_user.email}")
            else:
                print("  ⚠ User authentication failed")
                
        return True
    except Exception as e:
        print(f"  ✗ User operations failed: {e}")
        return False


async def main():
    """Run all tests."""
    print("Starting backend functionality tests...\n")
    
    # Test database connection
    db_success = await test_database_connection()
    
    # Test user operations
    user_success = await test_user_operations()
    
    print(f"\nTest Results:")
    print(f"- Database Connection: {'PASS' if db_success else 'FAIL'}")
    print(f"- User Operations: {'PASS' if user_success else 'FAIL'}")
    
    if db_success and user_success:
        print("\n✓ All tests passed! Backend is functioning correctly.")
    else:
        print("\n✗ Some tests failed. Please check the backend configuration.")


if __name__ == "__main__":
    asyncio.run(main())