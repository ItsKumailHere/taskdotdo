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