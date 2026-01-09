from sqlmodel import Session
from typing import Optional
from ..models.user_preferences import UserPreferences, UserPreferencesBase
from ..schemas.user_preferences import UserPreferencesUpdate


def get_user_preferences(session: Session, user_id: str) -> Optional[UserPreferences]:
    """Get user preferences by user ID."""
    return session.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()


def create_user_preferences(session: Session, user_id: str, preferences: UserPreferencesBase) -> UserPreferences:
    """Create user preferences for a user."""
    db_preferences = UserPreferences(user_id=user_id, **preferences.dict())
    session.add(db_preferences)
    session.commit()
    session.refresh(db_preferences)
    return db_preferences


def update_user_preferences(
    session: Session, 
    user_id: str, 
    preferences_update: UserPreferencesUpdate
) -> Optional[UserPreferences]:
    """Update user preferences."""
    db_preferences = session.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
    
    if not db_preferences:
        return None
    
    # Update only the fields that were provided
    update_data = preferences_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_preferences, field, value)
    
    session.add(db_preferences)
    session.commit()
    session.refresh(db_preferences)
    return db_preferences


def create_default_user_preferences(session: Session, user_id: str) -> UserPreferences:
    """Create default user preferences for a user."""
    from ..models.user_preferences import UserPreferences as UserPreferencesModel
    db_preferences = UserPreferencesModel(user_id=user_id)
    session.add(db_preferences)
    session.commit()
    session.refresh(db_preferences)
    return db_preferences