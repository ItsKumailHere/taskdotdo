"""
Users API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from ...database.session import get_session
from ...models.user import User
from ...schemas.user import UserPublic, UserUpdate
from ...auth.jwt import get_current_user



router = APIRouter()


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get a specific user by ID.
    """
    # For now, only allow users to get their own profile
    if user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user"
        )

    return UserPublic.model_validate(current_user)


@router.put("/{user_id}", response_model=UserPublic)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a user's information.
    """
    # For now, only allow users to update their own profile
    if user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    # Update user fields if provided
    if user_update.name is not None:
        current_user.name = user_update.name
    if user_update.email is not None:
        current_user.email = user_update.email
    if user_update.password is not None:
        from ...models.user import get_password_hash
        current_user.hashed_password = get_password_hash(user_update.password)
    
    # Update the updated_at timestamp
    from datetime import datetime
    current_user.updated_at = datetime.utcnow()
    
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)

    return UserPublic.model_validate(current_user)