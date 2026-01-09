from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
import re


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    username: str
    password_confirm: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        return v

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 30:
            raise ValueError('Username must be between 3 and 30 characters')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain alphanumeric characters and underscores')
        
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    created_at: datetime