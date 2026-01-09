from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import datetime
from app.database.session import get_session
from app.models.user import User
from app.schemas.user import UserInDB, UserUpdate, UserPreferencesUpdate
from app.services.user_service import get_user_by_id, update_user, update_user_preferences
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserInDB)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserInDB)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    updated_user = update_user(session, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user


@router.put("/me/preferences", response_model=dict)
def update_user_preferences_me(
    preferences_update: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    updated_user = update_user_preferences(session, current_user.id, preferences_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return updated_user.preferences