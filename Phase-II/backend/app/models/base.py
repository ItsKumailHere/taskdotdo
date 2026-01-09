"""
Base models and entities that all stories depend on
"""
from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID, uuid4
from sqlmodel import Field


class BaseUUIDModel(SQLModel):
    """
    Base model that includes common fields for all models:
    - id: UUID primary key
    - created_at: timestamp when record was created
    - updated_at: timestamp when record was last updated
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class HealthCheck(BaseModel):
    """
    Simple health check response model
    """
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class BaseTodo(SQLModel):
    """
    Base model for todo items
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class TodoCreate(BaseTodo):
    """
    Model for creating a new todo
    """
    pass


class TodoUpdate(SQLModel):
    """
    Model for updating a todo
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)


class TodoPublic(BaseTodo):
    """
    Public representation of a todo
    """
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None