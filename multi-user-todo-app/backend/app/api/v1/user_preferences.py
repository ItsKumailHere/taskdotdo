from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Optional
from ...database import get_session
from ...models.user import User
from ...api.deps import get_current_user
from ...services.user_preferences_service import (
    get_user_preferences,
    create_default_user_preferences,
    update_user_preferences
)
from ...schemas.user_preferences import UserPreferencesRead, UserPreferencesUpdate

router = APIRouter()


@router.get("/", response_model=UserPreferencesRead)
async def get_user_preferences_endpoint(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    preferences = get_user_preferences(session, current_user.id)
    if not preferences:
        # Create default preferences if they don't exist
        preferences = create_default_user_preferences(session, current_user.id)
    return preferences


@router.put("/", response_model=UserPreferencesRead)
async def update_user_preferences_endpoint(
    preferences_update: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    updated_preferences = update_user_preferences(
        session, current_user.id, preferences_update
    )
    if not updated_preferences:
        # Create preferences if they don't exist
        from ...models.user_preferences import UserPreferencesBase
        from ...services.user_preferences_service import create_user_preferences

        # Create a base preferences object with the updates
        base_preferences = UserPreferencesBase()
        update_data = preferences_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(base_preferences, field, value)

        updated_preferences = create_user_preferences(session, current_user.id, base_preferences)

    return updated_preferences