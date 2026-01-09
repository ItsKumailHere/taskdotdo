"""Tag CRUD endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_session
from app.models.user import User
from app.schemas.tag import TagCreate, TagPublic, TagUpdate
from app.services.tag_service import TagService
from app.utils.errors import ConflictException

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post(
    "/",
    response_model=TagPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new tag",
)
async def create_tag(
    tag_data: TagCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new tag for the authenticated user.

    Args:
        tag_data: Tag creation data
        current_user: Authenticated user
        session: Database session

    Returns:
        Created tag

    Raises:
        400: Invalid input data
        409: Tag name already exists
    """
    try:
        tag = await TagService.create_tag(
            session=session,
            user_id=current_user.id,
            name=tag_data.name,
        )
        return tag
    except ConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.get(
    "/",
    response_model=list[TagPublic],
    summary="Get all tags",
)
async def get_tags(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get all tags for the authenticated user.

    Args:
        current_user: Authenticated user
        session: Database session

    Returns:
        List of tags
    """
    tags = await TagService.get_user_tags(
        session=session,
        user_id=current_user.id,
    )
    return tags


@router.get(
    "/{tag_id}",
    response_model=TagPublic,
    summary="Get a tag by ID",
)
async def get_tag(
    tag_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get a specific tag by ID (must belong to authenticated user).

    Args:
        tag_id: Tag ID
        current_user: Authenticated user
        session: Database session

    Returns:
        Tag details

    Raises:
        404: Tag not found
    """
    tag = await TagService.get_tag_by_id(
        session=session,
        tag_id=tag_id,
        user_id=current_user.id,
    )
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    return tag


@router.patch(
    "/{tag_id}",
    response_model=TagPublic,
    summary="Update a tag",
)
async def update_tag(
    tag_id: UUID,
    tag_data: TagUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update a tag (must belong to authenticated user).

    Args:
        tag_id: Tag ID
        tag_data: Updated tag data
        current_user: Authenticated user
        session: Database session

    Returns:
        Updated tag

    Raises:
        404: Tag not found
        409: Tag name already exists
    """
    tag = await TagService.get_tag_by_id(
        session=session,
        tag_id=tag_id,
        user_id=current_user.id,
    )
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    try:
        updated_tag = await TagService.update_tag(
            session=session,
            tag=tag,
            name=tag_data.name,
        )
        return updated_tag
    except ConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.delete(
    "/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a tag",
)
async def delete_tag(
    tag_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete a tag (must belong to authenticated user).

    Args:
        tag_id: Tag ID
        current_user: Authenticated user
        session: Database session

    Raises:
        404: Tag not found
    """
    tag = await TagService.get_tag_by_id(
        session=session,
        tag_id=tag_id,
        user_id=current_user.id,
    )
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    await TagService.delete_tag(session=session, tag=tag)
