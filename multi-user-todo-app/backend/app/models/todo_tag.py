from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

from . import BaseTimestampModel


class TodoTag(BaseTimestampModel, table=True):
    __tablename__ = "todo_tags"
    
    todo_id: UUID = Field(foreign_key="todos.id", primary_key=True, ondelete="CASCADE")
    tag_id: UUID = Field(foreign_key="tags.id", primary_key=True, ondelete="CASCADE")
    assigned_at: datetime = Field(default_factory=datetime.utcnow)