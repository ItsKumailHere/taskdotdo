from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.database.session import get_session
from app.models.user import User
from app.models.notification import Notification, NotificationCreate, NotificationUpdate
from app.services.notification_service import get_notifications, get_notification_by_id, create_notification, update_notification, delete_notification, get_upcoming_notifications
from app.utils.dependencies import get_current_user
from app.schemas.notification import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/", response_model=List[NotificationResponse])
def read_notifications(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    notifications = get_notifications(session=session, user_id=current_user.id)
    return notifications


@router.post("/", response_model=NotificationResponse)
def create_notification_item(
    notification: NotificationCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_notification = create_notification(
        session=session,
        notification_create=notification,
        user_id=current_user.id
    )
    return db_notification


@router.get("/{notification_id}", response_model=NotificationResponse)
def read_notification(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        notification_uuid = UUID(notification_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notification ID format")
    
    db_notification = get_notification_by_id(session=session, notification_id=notification_uuid, user_id=current_user.id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification


@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification_item(
    notification_id: str,
    notification_update: NotificationUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        notification_uuid = UUID(notification_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notification ID format")
    
    db_notification = update_notification(
        session=session,
        notification_id=notification_uuid,
        notification_update=notification_update,
        user_id=current_user.id
    )
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification


@router.delete("/{notification_id}")
def delete_notification_item(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        notification_uuid = UUID(notification_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notification ID format")
    
    success = delete_notification(session=session, notification_id=notification_uuid, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification deleted successfully"}


@router.get("/upcoming", response_model=List[NotificationResponse])
def read_upcoming_notifications(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    notifications = get_upcoming_notifications(session=session, user_id=current_user.id)
    return notifications