"""
Todo model for the TaskDo application
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID
from .base import BaseUUIDModel, BaseTodo


class Todo(BaseTodo, BaseUUIDModel, table=True):
    """
    Todo model for the database
    """
    __tablename__ = "todos"

    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    
    # Foreign key to user
    user_id: UUID = Field(foreign_key="users.id", nullable=False)