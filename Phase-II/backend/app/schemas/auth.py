"""
Authentication-related schemas
"""
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import enum


class UserRole(str, enum.Enum):
    """User roles for authorization"""
    USER = "user"
    ADMIN = "admin"


class UserLoginRequest(BaseModel):
    """Request schema for user login"""
    email: str
    password: str


from pydantic import BaseModel, EmailStr, field_validator


class UserRegisterRequest(BaseModel):
    """Request schema for user registration"""
    email: EmailStr
    name: str
    password: str
    role: UserRole = UserRole.USER

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(v) > 100:
            raise ValueError("Name must be no more than 100 characters long")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # Note: We allow longer passwords but handle truncation internally in the hashing function
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class TokenResponse(BaseModel):
    """Response schema for authentication tokens"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None