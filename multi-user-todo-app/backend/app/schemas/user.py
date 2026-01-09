from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str
    password_confirm: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None


class UserInDB(UserBase):
    id: UUID
    created_at: datetime
    last_login_at: Optional[datetime] = None
    preferences: dict = {"theme": "light"}
    is_active: bool = True


class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = None