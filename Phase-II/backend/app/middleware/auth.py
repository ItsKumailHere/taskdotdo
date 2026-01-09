"""
Authentication middleware for the TaskDo backend
"""
from typing import Callable, Optional
from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPBearer
from jose import jwt
from ..config.settings import settings
from ..models.user import User
from sqlmodel.ext.asyncio.session import AsyncSession
from ..database.session import get_session
from sqlmodel import select
import os


class AuthMiddleware:
    """
    Middleware to handle authentication for protected routes
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        
        # Extract token from header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # For non-protected routes, allow the request to continue
            # Protected routes will handle the missing token in their dependencies
            return await self.app(scope, receive, send)

        token = auth_header.split(" ")[1]
        
        try:
            # Decode JWT token
            SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", settings.BETTER_AUTH_SECRET)
            payload = jwt.decode(token, SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                
            # Add user info to request state for use in route handlers
            request.state.user_id = user_id
            
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Continue processing the request
        return await self.app(scope, receive, send)


# For backward compatibility, keeping the JWT utilities
async def get_current_user_from_token(token: str) -> Optional[User]:
    """
    Helper function to get current user from token
    """
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", settings.BETTER_AUTH_SECRET)
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            return None
        
        # Get user from database
        async for session in get_session():  # This won't work directly, need to adjust
            statement = select(User).where(User.id == user_id)
            result = await session.execute(statement)
            user = result.first()
            return user[0] if user else None
            
    except jwt.JWTError:
        return None