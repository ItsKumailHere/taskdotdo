"""Tag model for labeling todos."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.todo_tag import TodoTag
    from app.models.user import User


class Tag(SQLModel, table=True):
    """
    Tag model for labeling and categorizing todos.

    Attributes:
        id: Unique identifier (UUID)
        name: Tag name (1-50 chars, unique per user)
        user_id: Foreign key to User
        created_at: Timestamp of creation
    """

    __tablename__ = "tags"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    # Tag Name
    name: str = Field(
        min_length=1,
        max_length=50,
        nullable=False,
        index=True,
    )

    # Foreign Key to User
    user_id: UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,
    )

    # Timestamp
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tags")
    todo_tags: list["TodoTag"] = Relationship(
        back_populates="tag",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )
