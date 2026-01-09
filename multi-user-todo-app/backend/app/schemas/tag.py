from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = None


class TagInDB(TagBase):
    id: UUID
    user_id: UUID
    created_at: datetime


class TagResponse(TagInDB):
    pass