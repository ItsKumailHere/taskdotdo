"""Tag-related Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    """Schema for creating a tag."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Tag name (1-50 characters, unique per user)",
    )


class TagUpdate(BaseModel):
    """Schema for updating a tag."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Tag name (1-50 characters, unique per user)",
    )


class TagPublic(BaseModel):
    """Schema for public tag data."""

    id: UUID
    name: str
    user_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
