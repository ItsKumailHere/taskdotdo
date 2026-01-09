from sqlmodel import Session, select, func
from typing import List, Optional
from datetime import datetime
from app.models.todo import Todo, TodoCreate, TodoUpdate, TaskStatus
from app.models.tag import Tag
from app.models.category import Category
from app.models.todo_tag import TodoTag
from fastapi import HTTPException, status
import uuid


def get_todos(
    session: Session,
    user_id: uuid.UUID,
    status: Optional[TaskStatus] = None,
    sort_by: str = "created_at",
    order: str = "desc",
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> List[Todo]:
    query = select(Todo).where(Todo.user_id == user_id)

    # Apply status filter
    if status:
        if status == TaskStatus.COMPLETED:
            query = query.where(Todo.status == TaskStatus.COMPLETED)
        elif status == TaskStatus.PENDING:
            query = query.where(Todo.status == TaskStatus.PENDING)

    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (Todo.title.ilike(search_pattern)) |
            (Todo.description.ilike(search_pattern))
        )

    # Apply sorting
    if sort_by == "title":
        sort_field = Todo.title
    elif sort_by == "due_date":
        sort_field = Todo.due_date
    else:  # default to created_at
        sort_field = Todo.created_at

    if order == "asc":
        query = query.order_by(sort_field)
    else:
        query = query.order_by(sort_field.desc())

    query = query.offset(offset).limit(limit)

    return session.exec(query).all()


def get_todo_by_id(session: Session, todo_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Todo]:
    return session.exec(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    ).first()


def create_todo(session: Session, todo_create: TodoCreate, user_id: uuid.UUID) -> Todo:
    # Verify category belongs to user if provided
    if todo_create.category_id:
        category = session.exec(
            select(Category).where(
                Category.id == todo_create.category_id,
                Category.user_id == user_id
            )
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category does not exist or does not belong to user"
            )

    # Verify tags belong to user if provided
    if todo_create.tag_ids:
        tags = session.exec(
            select(Tag).where(
                Tag.id.in_(todo_create.tag_ids),
                Tag.user_id == user_id
            )
        ).all()
        if len(tags) != len(todo_create.tag_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more tags do not exist or do not belong to user"
            )

    # Create the todo
    db_todo = Todo(
        title=todo_create.title,
        description=todo_create.description,
        status=todo_create.status,
        due_date=todo_create.due_date,
        user_id=user_id,
        category_id=todo_create.category_id
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    # Associate tags if provided
    if todo_create.tag_ids:
        for tag_id in todo_create.tag_ids:
            todo_tag = TodoTag(todo_id=db_todo.id, tag_id=tag_id)
            session.add(todo_tag)
        session.commit()

    # Refresh to get updated tags
    db_todo = session.exec(
        select(Todo).where(Todo.id == db_todo.id)
    ).first()

    return db_todo


def update_todo(session: Session, todo_id: uuid.UUID, todo_update: TodoUpdate, user_id: uuid.UUID) -> Optional[Todo]:
    db_todo = session.exec(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    ).first()

    if not db_todo:
        return None

    # Update fields if provided
    if todo_update.title is not None:
        db_todo.title = todo_update.title
    if todo_update.description is not None:
        db_todo.description = todo_update.description
    if todo_update.status is not None:
        db_todo.status = todo_update.status
        if todo_update.status == TaskStatus.COMPLETED and not db_todo.completed_at:
            db_todo.completed_at = datetime.utcnow()
        elif todo_update.status == TaskStatus.PENDING:
            db_todo.completed_at = None
    if todo_update.due_date is not None:
        db_todo.due_date = todo_update.due_date
    if todo_update.category_id is not None:
        # Verify category belongs to user
        if todo_update.category_id:
            category = session.exec(
                select(Category).where(
                    Category.id == todo_update.category_id,
                    Category.user_id == user_id
                )
            ).first()
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category does not exist or does not belong to user"
                )
        db_todo.category_id = todo_update.category_id

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    # Handle tag updates if provided
    if todo_update.tag_ids is not None:
        # Remove existing tags
        existing_tags = session.exec(
            select(TodoTag).where(TodoTag.todo_id == todo_id)
        ).all()
        for tag in existing_tags:
            session.delete(tag)

        # Add new tags
        if todo_update.tag_ids:
            # Verify tags belong to user
            tags = session.exec(
                select(Tag).where(
                    Tag.id.in_(todo_update.tag_ids),
                    Tag.user_id == user_id
                )
            ).all()
            if len(tags) != len(todo_update.tag_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more tags do not exist or do not belong to user"
                )

            for tag_id in todo_update.tag_ids:
                todo_tag = TodoTag(todo_id=db_todo.id, tag_id=tag_id)
                session.add(todo_tag)

        session.commit()
        session.refresh(db_todo)

    return db_todo


def delete_todo(session: Session, todo_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    db_todo = session.exec(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    ).first()
    
    if not db_todo:
        return False
    
    session.delete(db_todo)
    session.commit()
    return True