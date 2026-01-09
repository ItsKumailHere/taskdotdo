"""Todo service for todo-related business logic."""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.todo import Todo
from app.utils.errors import NotFoundException


class TodoService:
    """Service class for todo operations."""

    @staticmethod
    async def create_todo(
        session: AsyncSession,
        user_id: UUID,
        description: str,
        due_date: Optional[datetime] = None,
        category_id: Optional[UUID] = None,
    ) -> Todo:
        """
        Create a new todo.

        Args:
            session: Database session
            user_id: User ID
            description: Todo description
            due_date: Optional due date
            category_id: Optional category ID

        Returns:
            Created todo
        """
        todo = Todo(
            id=uuid4(),
            description=description,
            due_date=due_date,
            completed=False,
            created_at=datetime.now(timezone.utc),
            user_id=user_id,
            category_id=category_id,
        )

        session.add(todo)
        await session.commit()
        await session.refresh(todo)

        return todo

    @staticmethod
    async def get_user_todos(
        session: AsyncSession,
        user_id: UUID,
        completed: Optional[bool] = None,
        category_id: Optional[UUID] = None,
    ) -> list[Todo]:
        """
        Get all todos for a user with optional filters.

        Args:
            session: Database session
            user_id: User ID
            completed: Optional completion status filter
            category_id: Optional category filter

        Returns:
            List of todos
        """
        statement = select(Todo).where(Todo.user_id == user_id)

        if completed is not None:
            statement = statement.where(Todo.completed == completed)

        if category_id is not None:
            statement = statement.where(Todo.category_id == category_id)

        statement = statement.order_by(Todo.created_at.desc())

        result = await session.exec(statement)
        return result.all()

    @staticmethod
    async def get_todo_by_id(
        session: AsyncSession,
        todo_id: UUID,
        user_id: UUID,
    ) -> Optional[Todo]:
        """
        Get a specific todo by ID (must belong to user).

        Args:
            session: Database session
            todo_id: Todo ID
            user_id: User ID

        Returns:
            Todo if found, None otherwise
        """
        statement = select(Todo).where(
            Todo.id == todo_id,
            Todo.user_id == user_id,
        )
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def update_todo(
        session: AsyncSession,
        todo: Todo,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        completed: Optional[bool] = None,
        category_id: Optional[UUID] = None,
    ) -> Todo:
        """
        Update a todo.

        Args:
            session: Database session
            todo: Todo to update
            description: Optional new description
            due_date: Optional new due date
            completed: Optional new completion status
            category_id: Optional new category ID

        Returns:
            Updated todo
        """
        if description is not None:
            todo.description = description

        if due_date is not None:
            todo.due_date = due_date

        if completed is not None:
            todo.completed = completed
            if completed and not todo.completed_at:
                todo.completed_at = datetime.now(timezone.utc)
            elif not completed:
                todo.completed_at = None

        if category_id is not None:
            todo.category_id = category_id

        todo.updated_at = datetime.now(timezone.utc)

        session.add(todo)
        await session.commit()
        await session.refresh(todo)

        return todo

    @staticmethod
    async def delete_todo(
        session: AsyncSession,
        todo: Todo,
    ) -> None:
        """
        Delete a todo.

        Args:
            session: Database session
            todo: Todo to delete
        """
        await session.delete(todo)
        await session.commit()

    @staticmethod
    async def toggle_complete(
        session: AsyncSession,
        todo: Todo,
    ) -> Todo:
        """
        Toggle todo completion status.

        Args:
            session: Database session
            todo: Todo to toggle

        Returns:
            Updated todo
        """
        todo.completed = not todo.completed

        if todo.completed:
            todo.completed_at = datetime.now(timezone.utc)
        else:
            todo.completed_at = None

        todo.updated_at = datetime.now(timezone.utc)

        session.add(todo)
        await session.commit()
        await session.refresh(todo)

        return todo
