"""Category-related Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    """Schema for creating a category."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Category name (1-50 characters, unique per user)",
    )


class CategoryUpdate(BaseModel):
    """Schema for updating a category."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Category name (1-50 characters, unique per user)",
    )


class CategoryPublic(BaseModel):
    """Schema for public category data."""

    id: UUID
    name: str
    user_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
