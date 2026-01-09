from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class NotificationBase(BaseModel):
    message: str
    scheduled_at: datetime
    todo_id: Optional[UUID] = None


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    delivered: Optional[bool] = None


class NotificationInDB(NotificationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    delivered: bool
    delivered_at: Optional[datetime] = None


class NotificationResponse(NotificationInDB):
    pass