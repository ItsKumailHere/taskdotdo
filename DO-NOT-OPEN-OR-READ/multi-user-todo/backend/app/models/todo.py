"""Todo model for task management."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.notification import Notification
    from app.models.todo_tag import TodoTag
    from app.models.user import User


class Todo(SQLModel, table=True):
    """
    Todo model representing user tasks.

    Attributes:
        id: Unique identifier (UUID)
        description: Task description (1-500 chars)
        due_date: Optional due date and time
        completed: Completion status
        completed_at: Timestamp when marked complete (nullable)
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
        user_id: Foreign key to User
        category_id: Optional foreign key to Category
    """

    __tablename__ = "todos"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    # Todo Content
    description: str = Field(
        min_length=1,
        max_length=500,
        nullable=False,
    )

    # Due Date
    due_date: Optional[datetime] = Field(
        default=None,
        nullable=True,
        index=True,  # Index for querying upcoming todos
    )

    # Completion Status
    completed: bool = Field(
        default=False,
        nullable=False,
        index=True,  # Index for filtering by completion status
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
    )

    # Foreign Keys
    user_id: UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,  # Critical index for multi-tenant queries
    )
    category_id: Optional[UUID] = Field(
        default=None,
        foreign_key="categories.id",
        nullable=True,
        index=True,
    )

    # Relationships
    user: Optional["User"] = Relationship(back_populates="todos")
    category: Optional["Category"] = Relationship(back_populates="todos")
    todo_tags: list["TodoTag"] = Relationship(
        back_populates="todo",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )
    notifications: list["Notification"] = Relationship(
        back_populates="todo",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )
