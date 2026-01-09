"""Common dependencies for API endpoints."""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.dependencies import get_current_active_user, get_current_user
from app.database.session import get_session
from app.models.user import User

# Type aliases for cleaner endpoint signatures
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]
