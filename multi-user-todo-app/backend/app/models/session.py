from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

from . import BaseTimestampModel


class SessionBase(SQLModel):
    user_id: UUID
    session_token: str
    device_fingerprint: str
    expires_at: datetime


class Session(SessionBase, BaseTimestampModel, table=True):
    __tablename__ = "sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    session_token: str = Field(unique=True, max_length=255)
    device_fingerprint: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    is_active: bool = Field(default=True)

    # Relationship
    user: Optional[User] = Relationship(back_populates="sessions")


class SessionCreate(SessionBase):
    pass


class SessionRead(SessionBase):
    id: UUID
    created_at: datetime
    is_active: bool