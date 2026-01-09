"""
User-related schemas
"""
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    """User roles for authorization"""
    USER = "user"
    ADMIN = "admin"


class UserBase(BaseModel):
    """Base schema for user with common fields"""
    email: str
    name: str
    role: UserRole = UserRole.USER

    model_config = {"from_attributes": True}


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    model_config = {"from_attributes": True}


class UserPublic(UserBase):
    """Public representation of a user (without sensitive data)"""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_verified: bool = False
    is_active: bool = True

    model_config = {"from_attributes": True}


class UserInternal(UserBase):
    """Internal representation of a user (with sensitive data)"""
    id: UUID
    hashed_password: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_verified: bool = False
    is_active: bool = True

    model_config = {"from_attributes": True}