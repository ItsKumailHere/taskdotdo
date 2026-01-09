from sqlmodel import Session, select
from typing import Optional
from app.models.user import User, UserUpdate, UserPreferencesUpdate
from app.schemas.user import UserCreate
from app.services.auth_service import get_password_hash
from fastapi import HTTPException, status
import uuid


def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
    return session.exec(select(User).where(User.id == user_id)).first()


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()


def update_user(session: Session, user_id: uuid.UUID, user_update: UserUpdate) -> Optional[User]:
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return None
    
    # Update fields if provided
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.username is not None:
        user.username = user_update.username
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user_preferences(session: Session, user_id: uuid.UUID, preferences_update: UserPreferencesUpdate) -> Optional[User]:
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return None
    
    # Update preferences
    if user.preferences is None:
        user.preferences = {}
    
    if preferences_update.theme is not None:
        user.preferences["theme"] = preferences_update.theme
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: uuid.UUID) -> bool:
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return False
    
    session.delete(user)
    session.commit()
    return True


def create_user(session: Session, user_create: UserCreate) -> User:
    # Check if user already exists
    existing_user = get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = session.exec(
        select(User).where(User.username == user_create.username)
    ).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Verify password confirmation matches
    if user_create.password != user_create.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user_create.password)
    
    # Create the user object
    db_user = User(
        email=user_create.email,
        username=user_create.username,
        password_hash=hashed_password
    )
    
    # Add to session and commit
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user