from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from app.database.session import get_session
from app.models.user import User
from app.models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from app.services.todo_service import get_todos, get_todo_by_id, create_todo, update_todo, delete_todo
from app.utils.dependencies import get_current_user
from app.schemas.todo import TodoResponse, TodoQueryParams, TaskStatus
from uuid import UUID

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=List[TodoResponse])
def read_todos(
    status_param: Optional[TaskStatus] = Query(None, alias="status"),
    sort_by: str = Query("created_at", description="Sort by field (created_at, title, due_date)"),
    order: str = Query("desc", description="Sort order (asc, desc)"),
    search: Optional[str] = Query(None, description="Search term for title or description"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Calculate offset based on page and limit
    offset = (page - 1) * limit

    todos = get_todos(
        session=session,
        user_id=current_user.id,
        status=status_param,
        sort_by=sort_by,
        order=order,
        search=search,
        limit=limit,
        offset=offset
    )
    return todos


@router.post("/", response_model=TodoResponse)
def create_todo_item(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_todo = create_todo(
        session=session,
        todo_create=todo,
        user_id=current_user.id
    )
    return db_todo


@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        todo_uuid = UUID(todo_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID format")
    
    db_todo = get_todo_by_id(session=session, todo_id=todo_uuid, user_id=current_user.id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo_item(
    todo_id: str,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        todo_uuid = UUID(todo_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID format")
    
    db_todo = update_todo(
        session=session,
        todo_id=todo_uuid,
        todo_update=todo_update,
        user_id=current_user.id
    )
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.delete("/{todo_id}")
def delete_todo_item(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        todo_uuid = UUID(todo_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID format")
    
    success = delete_todo(session=session, todo_id=todo_uuid, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}