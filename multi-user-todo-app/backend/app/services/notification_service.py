from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.models.notification import Notification, NotificationCreate, NotificationUpdate
from fastapi import HTTPException, status
import uuid


def get_notifications(session: Session, user_id: uuid.UUID) -> List[Notification]:
    return session.exec(
        select(Notification).where(Notification.user_id == user_id)
    ).all()


def get_notification_by_id(session: Session, notification_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Notification]:
    return session.exec(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == user_id
        )
    ).first()


def create_notification(session: Session, notification_create: NotificationCreate, user_id: uuid.UUID) -> Notification:
    # If todo_id is provided, verify it belongs to the user
    if notification_create.todo_id:
        from app.models.todo import Todo
        todo = session.exec(
            select(Todo).where(
                Todo.id == notification_create.todo_id,
                Todo.user_id == user_id
            )
        ).first()
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todo does not exist or does not belong to user"
            )
    
    db_notification = Notification(
        user_id=user_id,
        message=notification_create.message,
        scheduled_at=notification_create.scheduled_at,
        todo_id=notification_create.todo_id
    )
    
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    
    return db_notification


def update_notification(session: Session, notification_id: uuid.UUID, notification_update: NotificationUpdate, user_id: uuid.UUID) -> Optional[Notification]:
    db_notification = session.exec(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == user_id
        )
    ).first()
    
    if not db_notification:
        return None
    
    if notification_update.delivered is not None:
        db_notification.delivered = notification_update.delivered
        if notification_update.delivered and not db_notification.delivered_at:
            db_notification.delivered_at = datetime.utcnow()
    
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    
    return db_notification


def delete_notification(session: Session, notification_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    db_notification = session.exec(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == user_id
        )
    ).first()
    
    if not db_notification:
        return False
    
    session.delete(db_notification)
    session.commit()
    return True


def get_upcoming_notifications(session: Session, user_id: uuid.UUID) -> List[Notification]:
    """Get notifications that are scheduled for the future and not yet delivered"""
    return session.exec(
        select(Notification).where(
            Notification.user_id == user_id,
            Notification.scheduled_at > datetime.utcnow(),
            Notification.delivered == False
        )
    ).all()