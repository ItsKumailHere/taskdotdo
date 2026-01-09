"""Authentication endpoints."""

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import CurrentActiveUser, SessionDep
from app.schemas.auth import AuthResponse, UserLogin, UserPublic, UserRegister
from app.services.auth_service import AuthService
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email, password, and username",
)
async def register(
    user_data: UserRegister,
    session: SessionDep,
) -> AuthResponse:
    """
    Register a new user account.

    Returns:
        - **access_token**: JWT token for authentication
        - **token_type**: Always "bearer"
        - **user**: User profile data
        - **expires_at**: Token expiration timestamp
    """
    logger.info(f"Registration attempt for email: {user_data.email}")

    user, access_token, expires_at = await AuthService.register_user(
        session=session,
        email=user_data.email,
        password=user_data.password,
        username=user_data.username,
    )

    logger.info(f"User registered successfully: {user.id}")

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserPublic.model_validate(user),
        expires_at=expires_at,
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login user",
    description="Authenticate user with email and password",
)
async def login(
    credentials: UserLogin,
    session: SessionDep,
) -> AuthResponse:
    """
    Authenticate user and return access token.

    Returns:
        - **access_token**: JWT token for authentication
        - **token_type**: Always "bearer"
        - **user**: User profile data
        - **expires_at**: Token expiration timestamp
    """
    logger.info(f"Login attempt for email: {credentials.email}")

    user, access_token, expires_at = await AuthService.authenticate_user(
        session=session,
        email=credentials.email,
        password=credentials.password,
    )

    logger.info(f"User logged in successfully: {user.id}")

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserPublic.model_validate(user),
        expires_at=expires_at,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout user",
    description="Logout current user (client should discard token)",
)
async def logout(
    current_user: CurrentActiveUser,
) -> None:
    """
    Logout user.

    Note: With JWT, logout is handled client-side by discarding the token.
    This endpoint exists for consistency and future session management.
    """
    logger.info(f"User logged out: {current_user.id}")
    return None


@router.get(
    "/me",
    response_model=UserPublic,
    summary="Get current user",
    description="Get the authenticated user's profile",
)
async def get_current_user_profile(
    current_user: CurrentActiveUser,
) -> UserPublic:
    """
    Get current authenticated user's profile.

    Returns:
        User profile data
    """
    return UserPublic.model_validate(current_user)
