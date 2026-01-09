"""TodoTag junction model for many-to-many relationship between Todo and Tag."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.tag import Tag
    from app.models.todo import Todo


class TodoTag(SQLModel, table=True):
    """
    TodoTag junction table for many-to-many relationship.

    Attributes:
        todo_id: Foreign key to Todo
        tag_id: Foreign key to Tag
        assigned_at: Timestamp when tag was assigned
    """

    __tablename__ = "todo_tags"

    # Composite Primary Key
    todo_id: UUID = Field(
        foreign_key="todos.id",
        primary_key=True,
        nullable=False,
        index=True,
    )
    tag_id: UUID = Field(
        foreign_key="tags.id",
        primary_key=True,
        nullable=False,
        index=True,
    )

    # Timestamp
    assigned_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    todo: Optional["Todo"] = Relationship(back_populates="todo_tags")
    tag: Optional["Tag"] = Relationship(back_populates="todo_tags")
