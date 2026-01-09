from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
from app.models.user import User, UserCreate
from app.config.settings import settings
from app.schemas.auth import UserLogin
from app.schemas.user import UserInDB
import uuid


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()


def create_user(session: Session, user_create: UserCreate) -> User:
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


def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
    return session.exec(select(User).where(User.id == user_id)).first()