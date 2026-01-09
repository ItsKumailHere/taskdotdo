"""Notification model for due date alerts."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.todo import Todo
    from app.models.user import User


class Notification(SQLModel, table=True):
    """
    Notification model for browser-based alerts.

    Attributes:
        id: Unique identifier (UUID)
        user_id: Foreign key to User
        todo_id: Optional foreign key to Todo
        message: Notification message (max 255 chars)
        scheduled_at: When notification should be shown
        delivered: Whether notification was delivered
        delivered_at: When notification was delivered (nullable)
        created_at: Timestamp of creation
    """

    __tablename__ = "notifications"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    # Foreign Keys
    user_id: UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,
    )
    todo_id: Optional[UUID] = Field(
        default=None,
        foreign_key="todos.id",
        nullable=True,
        index=True,
    )

    # Notification Content
    message: str = Field(
        max_length=255,
        nullable=False,
    )

    # Scheduling
    scheduled_at: datetime = Field(
        nullable=False,
        index=True,  # Index for querying pending notifications
    )

    # Delivery Status
    delivered: bool = Field(
        default=False,
        nullable=False,
        index=True,
    )
    delivered_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
    )

    # Timestamp
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user: Optional["User"] = Relationship(back_populates="notifications")
    todo: Optional["Todo"] = Relationship(back_populates="notifications")
