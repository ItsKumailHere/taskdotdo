from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

from . import BaseTimestampModel
from .todo_tag import TodoTag


class TagBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    user_id: UUID


class Tag(TagBase, BaseTimestampModel, table=True):
    __tablename__ = "tags"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=50)
    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE")

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tags")
    todos: List["Todo"] = Relationship(back_populates="tags", link_model=TodoTag)


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: UUID
    created_at: datetime


class TagUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)