"""Todo CRUD endpoints."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_session
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoPublic, TodoUpdate, TodoWithTags
from app.services.todo_service import TodoService
from app.utils.errors import NotFoundException

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post(
    "/",
    response_model=TodoPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo",
)
async def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new todo for the authenticated user.

    Args:
        todo_data: Todo creation data
        current_user: Authenticated user
        session: Database session

    Returns:
        Created todo

    Raises:
        400: Invalid input data
    """
    todo = await TodoService.create_todo(
        session=session,
        user_id=current_user.id,
        description=todo_data.description,
        due_date=todo_data.due_date,
        category_id=todo_data.category_id,
    )
    return todo


@router.get(
    "/",
    response_model=list[TodoPublic],
    summary="Get all todos",
)
async def get_todos(
    completed: Optional[bool] = None,
    category_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get all todos for the authenticated user with optional filters.

    Args:
        completed: Filter by completion status (optional)
        category_id: Filter by category (optional)
        current_user: Authenticated user
        session: Database session

    Returns:
        List of todos matching the filters
    """
    todos = await TodoService.get_user_todos(
        session=session,
        user_id=current_user.id,
        completed=completed,
        category_id=category_id,
    )
    return todos


@router.get(
    "/{todo_id}",
    response_model=TodoPublic,
    summary="Get a todo by ID",
)
async def get_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get a specific todo by ID (must belong to authenticated user).

    Args:
        todo_id: Todo ID
        current_user: Authenticated user
        session: Database session

    Returns:
        Todo details

    Raises:
        404: Todo not found
    """
    todo = await TodoService.get_todo_by_id(
        session=session,
        todo_id=todo_id,
        user_id=current_user.id,
    )
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    return todo


@router.patch(
    "/{todo_id}",
    response_model=TodoPublic,
    summary="Update a todo",
)
async def update_todo(
    todo_id: UUID,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update a todo (must belong to authenticated user).

    Args:
        todo_id: Todo ID
        todo_data: Updated todo data
        current_user: Authenticated user
        session: Database session

    Returns:
        Updated todo

    Raises:
        404: Todo not found
        400: Invalid input data
    """
    todo = await TodoService.get_todo_by_id(
        session=session,
        todo_id=todo_id,
        user_id=current_user.id,
    )
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    updated_todo = await TodoService.update_todo(
        session=session,
        todo=todo,
        description=todo_data.description,
        due_date=todo_data.due_date,
        completed=todo_data.completed,
        category_id=todo_data.category_id,
    )
    return updated_todo


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
)
async def delete_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete a todo (must belong to authenticated user).

    Args:
        todo_id: Todo ID
        current_user: Authenticated user
        session: Database session

    Raises:
        404: Todo not found
    """
    todo = await TodoService.get_todo_by_id(
        session=session,
        todo_id=todo_id,
        user_id=current_user.id,
    )
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    await TodoService.delete_todo(session=session, todo=todo)


@router.post(
    "/{todo_id}/toggle",
    response_model=TodoPublic,
    summary="Toggle todo completion",
)
async def toggle_todo_complete(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Toggle the completion status of a todo.

    Args:
        todo_id: Todo ID
        current_user: Authenticated user
        session: Database session

    Returns:
        Updated todo

    Raises:
        404: Todo not found
    """
    todo = await TodoService.get_todo_by_id(
        session=session,
        todo_id=todo_id,
        user_id=current_user.id,
    )
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    updated_todo = await TodoService.toggle_complete(session=session, todo=todo)
    return updated_todo
