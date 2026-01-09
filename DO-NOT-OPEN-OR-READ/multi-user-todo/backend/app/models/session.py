"""Session model for user session management."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class Session(SQLModel, table=True):
    """
    Session model for managing user sessions.

    Implements single-device login restriction and 90-day expiration.

    Attributes:
        id: Unique identifier (UUID)
        user_id: Foreign key to User
        session_token: Unique session identifier
        device_fingerprint: Device identifier for single-device restriction
        created_at: Timestamp of session creation
        expires_at: Timestamp when session expires
        is_active: Session active status
    """

    __tablename__ = "sessions"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    # Foreign Key to User
    user_id: UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,
    )

    # Session Identification
    session_token: str = Field(
        unique=True,
        nullable=False,
        index=True,  # Index for fast session lookups
    )
    device_fingerprint: str = Field(
        nullable=False,
        index=True,  # Index for checking existing sessions per device
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    expires_at: datetime = Field(
        nullable=False,
        index=True,  # Index for cleaning up expired sessions
    )

    # Session Status
    is_active: bool = Field(
        default=True,
        nullable=False,
        index=True,
    )

    # Relationships
    user: Optional["User"] = Relationship(back_populates="sessions")
