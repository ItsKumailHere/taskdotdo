"""FastAPI dependencies for authentication and authorization."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.jwt import decode_access_token
from app.database.session import get_session
from app.models.user import User

# Security scheme for extracting Bearer tokens
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    This dependency:
    1. Extracts the Bearer token from Authorization header
    2. Decodes and verifies the JWT token
    3. Extracts the user ID from the 'sub' claim
    4. Loads the user from the database
    5. Returns the User object

    Args:
        credentials: HTTP Bearer credentials from Authorization header
        session: Database session

    Returns:
        Authenticated User object

    Raises:
        HTTPException: 401 if token is invalid or user not found

    Usage:
        @app.get("/me")
        async def get_me(current_user: User = Depends(get_current_user)):
            return current_user
    """
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token
        payload = decode_access_token(token)

        # Extract user_id from 'sub' claim
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        # Convert string to UUID
        try:
            user_id = UUID(user_id_str)
        except ValueError:
            raise credentials_exception

    except JWTError as e:
        print(f"JWT decode error: {e}")
        raise credentials_exception

    # Load user from database
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    user = result.first()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependency to get the current active user.

    This is a stricter version of get_current_user that also checks
    if the user account is active.

    Args:
        current_user: User from get_current_user dependency

    Returns:
        Active User object

    Raises:
        HTTPException: 403 if user account is inactive

    Usage:
        @app.get("/todos")
        async def get_todos(user: User = Depends(get_current_active_user)):
            return user.todos
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )
    return current_user


# Type alias for convenience
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]
