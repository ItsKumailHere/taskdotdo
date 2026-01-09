"""User model for authentication and user management."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.notification import Notification
    from app.models.session import Session
    from app.models.tag import Tag
    from app.models.todo import Todo


class User(SQLModel, table=True):
    """
    User model representing registered users.

    Attributes:
        id: Unique identifier (UUID)
        email: User's email address (unique, max 254 chars)
        password_hash: Hashed password (max 128 chars)
        username: Unique username (3-30 chars, alphanumeric + underscores)
        created_at: Timestamp of account creation
        last_login_at: Timestamp of last login (nullable)
        preferences: JSON object with UI preferences (theme, language, etc.)
        is_active: Account active status
        session_token: Current session identifier (nullable)
    """

    __tablename__ = "users"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    # Authentication Fields
    email: str = Field(
        max_length=254,
        unique=True,
        index=True,
        nullable=False,
    )
    password_hash: str = Field(
        max_length=128,
        nullable=False,
    )
    username: str = Field(
        min_length=3,
        max_length=30,
        unique=True,
        index=True,
        nullable=False,
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    last_login_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )

    # User Preferences (stored as JSON)
    preferences: dict = Field(
        default={"theme": "light"},
        sa_column=Column(JSON, nullable=False),
    )

    # Account Status
    is_active: bool = Field(
        default=True,
        nullable=False,
    )

    # Current Session Token
    session_token: Optional[str] = Field(
        default=None,
        nullable=True,
    )

    # Relationships
    todos: list["Todo"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )
    tags: list["Tag"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )
    categories: list["Category"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )
    notifications: list["Notification"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )
    sessions: list["Session"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )
