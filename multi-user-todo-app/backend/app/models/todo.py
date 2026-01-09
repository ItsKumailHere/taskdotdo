from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from uuid import UUID, uuid4
import enum

from . import BaseTimestampModel
from .todo_tag import TodoTag

if TYPE_CHECKING:
    from .user import User
    from .category import Category
    from .tag import Tag
    from .notification import Notification


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    due_date: Optional[datetime] = Field(default=None)
    user_id: UUID = Field(nullable=False)
    category_id: Optional[UUID] = Field(default=None)


class Todo(TodoBase, BaseTimestampModel, table=True):
    __tablename__ = "todos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    due_date: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    category_id: Optional[UUID] = Field(default=None, foreign_key="categories.id", ondelete="SET NULL")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="todos")
    category: Optional["Category"] = Relationship(back_populates="todos")
    tags: List["Tag"] = Relationship(back_populates="todos", link_model=TodoTag)
    notifications: List["Notification"] = Relationship(back_populates="todo", cascade_delete=True)


class TodoCreate(TodoBase):
    tag_ids: Optional[List[UUID]] = []


class TodoRead(TodoBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    tag_ids: Optional[List[UUID]] = []


class TodoUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    category_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None