"""User service for user-related business logic."""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.password import hash_password
from app.models.user import User
from app.utils.errors import ConflictException, NotFoundException


class UserService:
    """Service class for user operations."""

    @staticmethod
    async def create_user(
        session: AsyncSession,
        email: str,
        password: str,
        username: str,
    ) -> User:
        """
        Create a new user.

        Args:
            session: Database session
            email: User email
            password: Plain text password (will be hashed)
            username: Username

        Returns:
            Created user

        Raises:
            ConflictException: If email or username already exists
        """
        # Check if email already exists
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        if result.first():
            raise ConflictException(
                "Email already registered",
                details={"field": "email"},
            )

        # Check if username already exists
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        if result.first():
            raise ConflictException(
                "Username already taken",
                details={"field": "username"},
            )

        # Create new user
        user = User(
            id=uuid4(),
            email=email,
            password_hash=hash_password(password),
            username=username,
            created_at=datetime.now(timezone.utc),
            preferences={"theme": "light"},
            is_active=True,
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    @staticmethod
    async def get_user_by_email(
        session: AsyncSession,
        email: str,
    ) -> Optional[User]:
        """
        Get user by email.

        Args:
            session: Database session
            email: User email

        Returns:
            User if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def get_user_by_id(
        session: AsyncSession,
        user_id: UUID,
    ) -> Optional[User]:
        """
        Get user by ID.

        Args:
            session: Database session
            user_id: User UUID

        Returns:
            User if found, None otherwise
        """
        statement = select(User).where(User.id == user_id)
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def update_last_login(
        session: AsyncSession,
        user: User,
    ) -> User:
        """
        Update user's last login timestamp.

        Args:
            session: Database session
            user: User to update

        Returns:
            Updated user
        """
        user.last_login_at = datetime.now(timezone.utc)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
