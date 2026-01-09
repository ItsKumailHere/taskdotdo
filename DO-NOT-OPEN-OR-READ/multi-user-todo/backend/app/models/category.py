"""Category model for organizing todos."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.todo import Todo
    from app.models.user import User


class Category(SQLModel, table=True):
    """
    Category model for grouping todos.

    Attributes:
        id: Unique identifier (UUID)
        name: Category name (1-50 chars, unique per user)
        user_id: Foreign key to User
        created_at: Timestamp of creation
    """

    __tablename__ = "categories"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    # Category Name
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
    user: Optional["User"] = Relationship(back_populates="categories")
    todos: list["Todo"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
