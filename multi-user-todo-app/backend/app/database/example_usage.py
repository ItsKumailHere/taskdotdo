"""
Example API router demonstrating the use of database sessions with FastAPI dependency injection.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db_session
from app.models import User, UserRead

router = APIRouter()


@router.get("/users", response_model=List[UserRead])
async def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve users with pagination.
    Demonstrates the use of the database session dependency.
    """
    try:
        # Query users from the database
        result = await db.execute(
            User.select().offset(skip).limit(limit)
        )
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a specific user by ID.
    Demonstrates the use of the database session dependency.
    """
    try:
        user = await db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")