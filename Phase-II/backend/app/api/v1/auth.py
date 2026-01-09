"""
Authentication API routes
"""
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from ...database.session import get_session
from ...schemas.user import UserPublic
from ...schemas.auth import UserRegisterRequest as UserCreate
from ...models.user import User
from ...auth.jwt import get_current_user

from ...services.auth_service import register_user as service_register_user, authenticate_user

from jose import jwt
import os


router = APIRouter()


@router.post("/register", response_model=UserPublic)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    """
    Register a new user.
    """
    # The register_user service function will raise HTTPException on error
    user = await service_register_user(session, user_data)
    return user


from ...schemas.auth import UserLoginRequest

@router.post("/login")
async def login_user(user_data: UserLoginRequest, session: AsyncSession = Depends(get_session)):
    """
    Authenticate user and return JWT token.
    """
    user = await authenticate_user(
        session,
        email=user_data.email,
        password=user_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-change-this-in-production")
    ALGORITHM = "HS256"
    
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value
    }
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserPublic.model_validate(user)
    }


@router.get("/me", response_model=UserPublic)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user info.
    """
    return UserPublic.model_validate(current_user)


@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Refresh the access token.
    """
    # Create a new JWT token with updated expiration
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-change-this-in-production")
    ALGORITHM = "HS256"

    # Create new token with fresh expiration
    from datetime import timedelta, datetime
    expire = datetime.utcnow() + timedelta(minutes=30)  # 30 minutes for refreshed token

    token_data = {
        "sub": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role.value,
        "exp": expire.timestamp()
    }

    new_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": new_token,
        "token_type": "bearer"
    }


from fastapi.security import HTTPAuthorizationCredentials
from ...auth.jwt import security


@router.post("/logout")
async def logout_user_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user)
):
    """
    Log out the current user by adding the token to a blacklist.
    """
    from ...services.auth_service import logout_user as service_logout_user

    token = credentials.credentials

    # Add token to blacklist
    success = await service_logout_user(current_user, token)

    if success:
        return {"message": "Successfully logged out"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to logout"
        )