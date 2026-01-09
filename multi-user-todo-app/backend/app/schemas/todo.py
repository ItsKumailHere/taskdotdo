from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
import enum


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    due_date: Optional[datetime] = None
    category_id: Optional[UUID] = None


class TodoCreate(TodoBase):
    tag_ids: Optional[List[UUID]] = []


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    category_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None


class TodoInDB(TodoBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime] = None
    tag_ids: Optional[List[UUID]] = []


class TodoResponse(TodoInDB):
    pass


class TodoQueryParams(BaseModel):
    status: Optional[TaskStatus] = None
    sort_by: str = "created_at"  # Options: created_at, title, due_date
    order: str = "desc"  # Options: asc, desc
    search: Optional[str] = None
    page: int = 1
    limit: int = 20