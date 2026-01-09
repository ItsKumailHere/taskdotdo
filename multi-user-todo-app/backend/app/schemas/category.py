from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None


class CategoryInDB(CategoryBase):
    id: UUID
    user_id: UUID
    created_at: datetime


class CategoryResponse(CategoryInDB):
    pass