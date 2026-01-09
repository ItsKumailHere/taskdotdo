"""Authentication-related Pydantic schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    """Schema for user registration request."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters)",
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        pattern="^[a-zA-Z0-9_]+$",
        description="Username (3-30 alphanumeric characters and underscores)",
    )


class UserLogin(BaseModel):
    """Schema for user login request."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserPublic(BaseModel):
    """Schema for public user data (safe to expose)."""

    id: UUID
    email: str
    username: str
    created_at: datetime
    last_login_at: Optional[datetime] = None
    preferences: dict = Field(default_factory=lambda: {"theme": "light"})
    is_active: bool

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    """Schema for authentication response with token."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserPublic = Field(..., description="Authenticated user data")
    expires_at: datetime = Field(..., description="Token expiration timestamp")
