from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg

from . import BaseTimestampModel
from .user_preferences import UserPreferences


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    is_active: bool = True


class User(UserBase, BaseTimestampModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=254)
    username: str = Field(unique=True, index=True, min_length=3, max_length=30)
    password_hash: str = Field(max_length=128)
    last_login_at: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True)
    session_token: Optional[str] = Field(default=None, max_length=255)

    # Relationships
    todos: List["Todo"] = Relationship(back_populates="user", cascade_delete=True)
    categories: List["Category"] = Relationship(back_populates="user", cascade_delete=True)
    tags: List["Tag"] = Relationship(back_populates="user", cascade_delete=True)
    notifications: List["Notification"] = Relationship(back_populates="user", cascade_delete=True)
    sessions: List["Session"] = Relationship(back_populates="user", cascade_delete=True)
    preferences: "UserPreferences" = Relationship(back_populates="user", cascade_delete=True)


class UserCreate(UserBase):
    password: str
    password_confirm: str


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    last_login_at: Optional[datetime] = None
    is_active: bool = True


class UserUpdate(SQLModel):
    email: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None


class UserUpdatePassword(SQLModel):
    current_password: str
    new_password: str
    new_password_confirm: str


# Note: UserPreferencesUpdate is now defined in the user_preferences module
# This is kept here for backward compatibility
class UserPreferencesUpdate(SQLModel):
    theme: Optional[str] = None