from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

from . import BaseTimestampModel


class CategoryBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    user_id: UUID


class Category(CategoryBase, BaseTimestampModel, table=True):
    __tablename__ = "categories"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=50)
    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE")

    # Relationships
    user: Optional[User] = Relationship(back_populates="categories")
    todos: List[Todo] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: UUID
    created_at: datetime


class CategoryUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)