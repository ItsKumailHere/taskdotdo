"""Todo-related Pydantic schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """Schema for creating a todo."""

    description: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Todo description (1-500 characters)",
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Optional due date and time",
    )
    category_id: Optional[UUID] = Field(
        None,
        description="Optional category ID",
    )


class TodoUpdate(BaseModel):
    """Schema for updating a todo."""

    description: Optional[str] = Field(
        None,
        min_length=1,
        max_length=500,
        description="Todo description (1-500 characters)",
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Due date and time",
    )
    completed: Optional[bool] = Field(
        None,
        description="Completion status",
    )
    category_id: Optional[UUID] = Field(
        None,
        description="Category ID (set to null to remove)",
    )


class TodoPublic(BaseModel):
    """Schema for public todo data."""

    id: UUID
    description: str
    due_date: Optional[datetime]
    completed: bool
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: UUID
    category_id: Optional[UUID]

    model_config = {"from_attributes": True}


class TodoWithTags(TodoPublic):
    """Schema for todo with tag IDs."""

    tag_ids: list[UUID] = Field(default_factory=list, description="List of tag IDs")
