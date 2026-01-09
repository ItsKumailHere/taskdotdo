"""
Todos API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from uuid import UUID

from ...database.session import get_session
from ...models.todo import Todo
from ...models.base import TodoCreate, TodoUpdate, TodoPublic
from ...models.user import User
from ...auth.jwt import get_current_user
from ...services.todo_service import (
    create_todo, get_todos_by_user, get_todo_by_id_and_user,
    update_todo, delete_todo, update_todo_status
)


router = APIRouter()


@router.get("/", response_model=List[TodoPublic])
async def get_todos(
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session),
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",  # Default sort by creation date
    sort_order: str = "desc"  # Default sort order descending
):
    """
    Get all todos for the current user with optional filtering and sorting.
    """
    # Validate sort parameters
    valid_sort_fields = {"created_at", "updated_at", "title", "completed"}
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort field. Valid fields: {', '.join(valid_sort_fields)}"
        )

    if sort_order not in {"asc", "desc"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sort_order must be either 'asc' or 'desc'"
        )

    todos = await get_todos_by_user(
        db_session=db_session,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        completed=completed,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return todos


@router.post("/", response_model=TodoPublic)
async def create_todo_endpoint(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session)
):
    """
    Create a new todo for the current user.
    """
    return await create_todo(
        db_session=db_session,
        todo_data=todo_data,
        user_id=current_user.id
    )


@router.get("/{todo_id}", response_model=TodoPublic)
async def get_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session)
):
    """
    Get a specific todo by ID.
    """
    todo = await get_todo_by_id_and_user(
        db_session=db_session,
        todo_id=todo_id,
        user_id=current_user.id
    )
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return TodoPublic.model_validate(todo)


@router.put("/{todo_id}", response_model=TodoPublic)
async def update_todo_endpoint(
    todo_id: UUID,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session)
):
    """
    Update a specific todo by ID.
    """
    updated_todo = await update_todo(
        db_session=db_session,
        todo_id=todo_id,
        user_id=current_user.id,
        todo_update=todo_update
    )
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return updated_todo


@router.patch("/{todo_id}/status", response_model=TodoPublic)
async def update_todo_status_endpoint(
    todo_id: UUID,
    completed: bool,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session)
):
    """
    Update the status of a specific todo by ID.
    """
    updated_todo = await update_todo_status(
        db_session=db_session,
        todo_id=todo_id,
        user_id=current_user.id,
        completed=completed
    )
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return updated_todo


@router.delete("/{todo_id}")
async def delete_todo_endpoint(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session)
):
    """
    Delete a specific todo by ID.
    """
    success = await delete_todo(
        db_session=db_session,
        todo_id=todo_id,
        user_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return {"message": "Todo deleted successfully"}