"""
JWT utilities for the TaskDo backend
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import HTTPException, status
import os
from ..config.settings import settings
from ..models.user import User


# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", settings.SECRET_KEY)
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token with the provided data
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the payload if valid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from a JWT token
    """
    payload = verify_token(token)
    if payload:
        user_id = payload.get("sub")
        return user_id
    return None


def get_current_user_from_token(token: str) -> Optional[User]:
    """
    Get the current user from a JWT token
    This function would typically fetch user details from the database
    based on the user ID in the token.
    """
    user_id = get_user_id_from_token(token)
    if user_id:
        # In a real implementation, you would fetch the user from the database
        # For now, we return a placeholder indicating the user was found
        return User(id=user_id, email="placeholder@example.com", name="Placeholder User", 
                   hashed_password="placeholder", created_at=datetime.utcnow())
    return None


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired
    """
    payload = verify_token(token)
    if payload:
        exp_time = payload.get("exp")
        if exp_time:
            return datetime.fromtimestamp(exp_time) < datetime.utcnow()
    return True  # If we can't verify the token, treat it as expired


def refresh_access_token(token: str) -> Optional[str]:
    """
    Refresh an access token if it's about to expire
    """
    payload = verify_token(token)
    if payload:
        # Check if the token is about to expire (within 5 minutes)
        exp_time = payload.get("exp")
        if exp_time:
            expiry_datetime = datetime.fromtimestamp(exp_time)
            if expiry_datetime - datetime.utcnow() < timedelta(minutes=5):
                # Create a new token with the same data
                user_id = payload.get("sub")
                email = payload.get("email")
                role = payload.get("role")
                
                new_data = {"sub": user_id, "email": email, "role": role}
                return create_access_token(data=new_data)
    
    return None