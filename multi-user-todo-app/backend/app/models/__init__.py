from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class BaseTimestampModel(SQLModel):
    """
    Base model that includes timestamp fields for all models
    """
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Import all models to register them with SQLModel metadata
# This is required for Alembic autogenerate to work properly
from . import user
from . import todo
from . import category
from . import tag
from . import todo_tag
from . import notification
from . import session

# Export commonly used models
from .user import User, UserCreate, UserRead, UserUpdate, UserUpdatePassword, UserPreferencesUpdate
from .todo import Todo, TodoCreate, TodoRead, TodoUpdate
from .category import Category, CategoryCreate, CategoryRead, CategoryUpdate
from .tag import Tag, TagCreate, TagRead, TagUpdate
from .notification import Notification, NotificationCreate, NotificationRead, NotificationUpdate
from .session import Session, SessionCreate, SessionRead