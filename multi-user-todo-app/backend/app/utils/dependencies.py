from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import Session
from app.database.session import get_session
from app.models.user import User
from app.config.settings import settings
from app.services.auth_service import get_user_by_id
from app.auth import verify_better_auth_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Updated dependency to verify Better Auth JWT tokens
    """
    return verify_better_auth_token(credentials, session)