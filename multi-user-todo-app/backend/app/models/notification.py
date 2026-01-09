from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

from . import BaseTimestampModel


class NotificationBase(SQLModel):
    user_id: UUID
    message: str = Field(max_length=255)
    scheduled_at: datetime
    todo_id: Optional[UUID] = None


class Notification(NotificationBase, BaseTimestampModel, table=True):
    __tablename__ = "notifications"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    todo_id: Optional[UUID] = Field(default=None, foreign_key="todos.id", ondelete="CASCADE")
    message: str = Field(max_length=255)
    scheduled_at: datetime
    delivered: bool = Field(default=False)
    delivered_at: Optional[datetime] = Field(default=None)

    # Relationships
    user: Optional[User] = Relationship(back_populates="notifications")
    todo: Optional[Todo] = Relationship(back_populates="notifications")


class NotificationCreate(NotificationBase):
    pass


class NotificationRead(NotificationBase):
    id: UUID
    created_at: datetime
    delivered: bool
    delivered_at: Optional[datetime] = None


class NotificationUpdate(SQLModel):
    delivered: Optional[bool] = None