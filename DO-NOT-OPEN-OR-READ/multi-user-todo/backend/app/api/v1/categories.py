"""Category CRUD endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_session
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryPublic, CategoryUpdate
from app.services.category_service import CategoryService
from app.utils.errors import ConflictException

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post(
    "/",
    response_model=CategoryPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
)
async def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new category for the authenticated user.

    Args:
        category_data: Category creation data
        current_user: Authenticated user
        session: Database session

    Returns:
        Created category

    Raises:
        400: Invalid input data
        409: Category name already exists
    """
    try:
        category = await CategoryService.create_category(
            session=session,
            user_id=current_user.id,
            name=category_data.name,
        )
        return category
    except ConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.get(
    "/",
    response_model=list[CategoryPublic],
    summary="Get all categories",
)
async def get_categories(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get all categories for the authenticated user.

    Args:
        current_user: Authenticated user
        session: Database session

    Returns:
        List of categories
    """
    categories = await CategoryService.get_user_categories(
        session=session,
        user_id=current_user.id,
    )
    return categories


@router.get(
    "/{category_id}",
    response_model=CategoryPublic,
    summary="Get a category by ID",
)
async def get_category(
    category_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get a specific category by ID (must belong to authenticated user).

    Args:
        category_id: Category ID
        current_user: Authenticated user
        session: Database session

    Returns:
        Category details

    Raises:
        404: Category not found
    """
    category = await CategoryService.get_category_by_id(
        session=session,
        category_id=category_id,
        user_id=current_user.id,
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


@router.patch(
    "/{category_id}",
    response_model=CategoryPublic,
    summary="Update a category",
)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update a category (must belong to authenticated user).

    Args:
        category_id: Category ID
        category_data: Updated category data
        current_user: Authenticated user
        session: Database session

    Returns:
        Updated category

    Raises:
        404: Category not found
        409: Category name already exists
    """
    category = await CategoryService.get_category_by_id(
        session=session,
        category_id=category_id,
        user_id=current_user.id,
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    try:
        updated_category = await CategoryService.update_category(
            session=session,
            category=category,
            name=category_data.name,
        )
        return updated_category
    except ConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category",
)
async def delete_category(
    category_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete a category (must belong to authenticated user).

    Args:
        category_id: Category ID
        current_user: Authenticated user
        session: Database session

    Raises:
        404: Category not found
    """
    category = await CategoryService.get_category_by_id(
        session=session,
        category_id=category_id,
        user_id=current_user.id,
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    await CategoryService.delete_category(session=session, category=category)
