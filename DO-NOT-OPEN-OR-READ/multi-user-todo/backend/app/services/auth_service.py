"""Authentication service for authentication-related business logic."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.jwt import create_access_token
from app.auth.password import verify_password
from app.config.settings import settings
from app.models.user import User
from app.services.user_service import UserService
from app.utils.errors import UnauthorizedException


class AuthService:
    """Service class for authentication operations."""

    @staticmethod
    async def authenticate_user(
        session: AsyncSession,
        email: str,
        password: str,
    ) -> tuple[User, str, datetime]:
        """
        Authenticate user with email and password.

        Args:
            session: Database session
            email: User email
            password: Plain text password

        Returns:
            Tuple of (user, access_token, expires_at)

        Raises:
            UnauthorizedException: If credentials are invalid
        """
        # Get user by email
        user = await UserService.get_user_by_email(session, email)

        if not user:
            raise UnauthorizedException("Invalid email or password")

        # Verify password
        if not verify_password(password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")

        # Check if user is active
        if not user.is_active:
            raise UnauthorizedException("Account is inactive")

        # Generate access token
        expires_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
        access_token = create_access_token(
            subject=user.id,
            expires_delta=expires_delta,
            additional_claims={"email": user.email},
        )

        # Calculate expiration time
        expires_at = datetime.now(timezone.utc) + expires_delta

        # Update last login
        await UserService.update_last_login(session, user)

        return user, access_token, expires_at

    @staticmethod
    async def register_user(
        session: AsyncSession,
        email: str,
        password: str,
        username: str,
    ) -> tuple[User, str, datetime]:
        """
        Register a new user.

        Args:
            session: Database session
            email: User email
            password: Plain text password
            username: Username

        Returns:
            Tuple of (user, access_token, expires_at)

        Raises:
            ConflictException: If email or username already exists
        """
        # Create user
        user = await UserService.create_user(
            session=session,
            email=email,
            password=password,
            username=username,
        )

        # Generate access token
        expires_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
        access_token = create_access_token(
            subject=user.id,
            expires_delta=expires_delta,
            additional_claims={"email": user.email},
        )

        # Calculate expiration time
        expires_at = datetime.now(timezone.utc) + expires_delta

        # Update last login
        await UserService.update_last_login(session, user)

        return user, access_token, expires_at
