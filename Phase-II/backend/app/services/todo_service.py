"""
Todo service layer
Handles business logic for todo operations
"""
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional, List
from uuid import UUID

from ..models.todo import Todo
from ..models.base import TodoCreate, TodoUpdate, TodoPublic
from ..models.user import User
from sqlmodel import select, and_
from datetime import datetime


async def create_todo(db_session: AsyncSession, todo_data: TodoCreate, user_id: UUID) -> TodoPublic:
    """
    Create a new todo for the specified user
    """
    db_todo = Todo(
        **todo_data.model_dump(),
        user_id=user_id
    )
    db_session.add(db_todo)
    await db_session.commit()
    await db_session.refresh(db_todo)

    # Convert to TodoPublic format
    return TodoPublic.model_validate(db_todo)


async def get_todos_by_user(
    db_session: AsyncSession,
    user_id: UUID,
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> List[TodoPublic]:
    """
    Retrieve all todos for a specific user with optional filtering and sorting
    """
    query = select(Todo).where(Todo.user_id == user_id)

    if completed is not None:
        query = query.where(Todo.completed == completed)

    # Apply sorting
    if sort_order == "asc":
        if sort_by == "title":
            query = query.order_by(Todo.title.asc())
        elif sort_by == "completed":
            query = query.order_by(Todo.completed.asc())
        elif sort_by == "updated_at":
            query = query.order_by(Todo.updated_at.asc() if Todo.updated_at is not None else Todo.created_at.asc())
        else:  # Default to created_at
            query = query.order_by(Todo.created_at.asc())
    else:  # desc
        if sort_by == "title":
            query = query.order_by(Todo.title.desc())
        elif sort_by == "completed":
            query = query.order_by(Todo.completed.desc())
        elif sort_by == "updated_at":
            query = query.order_by(Todo.updated_at.desc() if Todo.updated_at is not None else Todo.created_at.desc())
        else:  # Default to created_at
            query = query.order_by(Todo.created_at.desc())

    query = query.offset(skip).limit(limit)

    result = await db_session.execute(query)
    todos = result.scalars().all()

    # Convert to TodoPublic format
    return [TodoPublic.model_validate(todo) for todo in todos]


async def get_todo_by_id_and_user(db_session: AsyncSession, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
    """
    Retrieve a specific todo by ID for a specific user
    """
    query = select(Todo).where(and_(Todo.id == todo_id, Todo.user_id == user_id))
    result = await db_session.execute(query)
    return result.scalar_one_or_none()


async def update_todo(
    db_session: AsyncSession,
    todo_id: UUID,
    user_id: UUID,
    todo_update: TodoUpdate
) -> Optional[TodoPublic]:
    """
    Update a specific todo for a specific user
    """
    db_todo = await get_todo_by_id_and_user(db_session, todo_id, user_id)
    if not db_todo:
        return None

    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)

    # Use the same timezone-aware datetime as in the base model
    db_todo.updated_at = datetime.utcnow()

    db_session.add(db_todo)
    await db_session.commit()
    await db_session.refresh(db_todo)

    # Convert to TodoPublic format
    return TodoPublic.model_validate(db_todo)


async def delete_todo(db_session: AsyncSession, todo_id: UUID, user_id: UUID) -> bool:
    """
    Delete a specific todo for a specific user
    """
    db_todo = await get_todo_by_id_and_user(db_session, todo_id, user_id)
    if not db_todo:
        return False

    await db_session.delete(db_todo)
    await db_session.commit()
    return True


async def update_todo_status(
    db_session: AsyncSession,
    todo_id: UUID,
    user_id: UUID,
    completed: bool
) -> Optional[TodoPublic]:
    """
    Update the completion status of a specific todo for a specific user
    """
    db_todo = await get_todo_by_id_and_user(db_session, todo_id, user_id)
    if not db_todo:
        return None

    db_todo.completed = completed
    # Use the same timezone-aware datetime as in the base model
    db_todo.updated_at = datetime.utcnow()

    db_session.add(db_todo)
    await db_session.commit()
    await db_session.refresh(db_todo)

    # Convert to TodoPublic format
    return TodoPublic.model_validate(db_todo)