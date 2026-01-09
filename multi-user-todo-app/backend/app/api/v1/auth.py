from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from datetime import timedelta
from app.database.session import get_session
from app.schemas.auth import UserRegister, UserLogin, Token
from app.services.auth_service import authenticate_user, get_user_by_email, create_user
from app.services.user_service import get_user_by_email as get_user_by_email_service
from app.config.settings import settings
from app.models.user import User
from app.auth import verify_better_auth_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(user_register: UserRegister, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = get_user_by_email_service(session, user_register.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Verify password confirmation matches
    if user_register.password != user_register.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Create user
    db_user = create_user(session, user_register)

    # For Better Auth integration, we won't return a token here
    # Better Auth handles token creation on the frontend
    # Instead, we'll just return a success message
    return {"access_token": "", "token_type": "bearer", "message": "User registered successfully"}


@router.post("/login", response_model=Token)
def login(user_login: UserLogin, session: Session = Depends(get_session)):
    user = authenticate_user(session, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login time
    user.last_login_at = user_login.__dict__.get('timestamp', None)  # Will be updated with current time in model
    session.add(user)
    session.commit()

    # For Better Auth integration, we won't return a token here
    # Better Auth handles token creation on the frontend
    # Instead, we'll just return a success message
    return {"access_token": "", "token_type": "bearer", "message": "Login successful"}


@router.post("/logout")
def logout():
    # In a Better Auth setup, logout is handled on the frontend
    # For backend cleanup, we might want to invalidate sessions if stored
    # For now, we'll just return a success message
    return {"message": "Successfully logged out"}


# Endpoint to verify the Better Auth token and get user info
@router.get("/verify-token", response_model=User)
def verify_token(current_user: User = Depends(verify_better_auth_token)):
    """Verify the Better Auth token and return user information"""
    return current_user