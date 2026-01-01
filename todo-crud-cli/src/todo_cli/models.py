# Models for the Todo App
from enum import Enum
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

class Task(BaseModel):
    id: int
    description: str = Field(..., min_length=1, max_length=255)
    status: TaskStatus = TaskStatus.PENDING
