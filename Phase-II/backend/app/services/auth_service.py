"""
Authentication service layer
Handles business logic for authentication operations
"""
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional, Tuple
from ..models.user import User
from ..schemas.user import UserCreate as UserRegisterRequest
from ..models.user import get_password_hash, verify_password
from fastapi import HTTPException, status
from sqlmodel import select


async def register_user(session: AsyncSession, user_data: UserRegisterRequest) -> User:
    """
    Register a new user with hashed password
    """
    # Check if user with email already exists
    existing_user_statement = select(User).where(User.email == user_data.email)
    result = await session.exec(existing_user_statement)
    existing_user = result.first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create new user instance
    user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password,
        role=user_data.role
    )

    # Add to session and commit
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate user by email and password
    """
    # Find user by email
    statement = select(User).where(User.email == email)
    result = await session.exec(statement)
    user = result.first()

    # Verify user exists and password is correct
    if not user or not verify_password(password, user.hashed_password):
        return None

    return user


# In-memory token blacklist for demonstration purposes
# In production, use Redis or database for token blacklisting
token_blacklist = set()


async def logout_user(user: User, token: str) -> bool:
    """
    Logout user by adding token to blacklist
    """
    # Add token to blacklist
    token_blacklist.add(token)
    return True


def is_token_blacklisted(token: str) -> bool:
    """
    Check if token is in blacklist
    """
    return token in token_blacklist