"""Category service for category-related business logic."""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.category import Category
from app.utils.errors import ConflictException, NotFoundException


class CategoryService:
    """Service class for category operations."""

    @staticmethod
    async def create_category(
        session: AsyncSession,
        user_id: UUID,
        name: str,
    ) -> Category:
        """
        Create a new category.

        Args:
            session: Database session
            user_id: User ID
            name: Category name

        Returns:
            Created category

        Raises:
            ConflictException: If category name already exists for user
        """
        # Check if category name already exists for this user
        statement = select(Category).where(
            Category.user_id == user_id,
            Category.name == name,
        )
        result = await session.exec(statement)
        if result.first():
            raise ConflictException(
                f"Category '{name}' already exists",
                details={"field": "name"},
            )

        category = Category(
            id=uuid4(),
            name=name,
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
        )

        session.add(category)
        await session.commit()
        await session.refresh(category)

        return category

    @staticmethod
    async def get_user_categories(
        session: AsyncSession,
        user_id: UUID,
    ) -> list[Category]:
        """
        Get all categories for a user.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            List of categories
        """
        statement = select(Category).where(Category.user_id == user_id).order_by(Category.name)
        result = await session.exec(statement)
        return result.all()

    @staticmethod
    async def get_category_by_id(
        session: AsyncSession,
        category_id: UUID,
        user_id: UUID,
    ) -> Optional[Category]:
        """
        Get a specific category by ID (must belong to user).

        Args:
            session: Database session
            category_id: Category ID
            user_id: User ID

        Returns:
            Category if found, None otherwise
        """
        statement = select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id,
        )
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def update_category(
        session: AsyncSession,
        category: Category,
        name: str,
    ) -> Category:
        """
        Update a category.

        Args:
            session: Database session
            category: Category to update
            name: New name

        Returns:
            Updated category

        Raises:
            ConflictException: If new name already exists for user
        """
        # Check if new name conflicts with another category
        statement = select(Category).where(
            Category.user_id == category.user_id,
            Category.name == name,
            Category.id != category.id,
        )
        result = await session.exec(statement)
        if result.first():
            raise ConflictException(
                f"Category '{name}' already exists",
                details={"field": "name"},
            )

        category.name = name

        session.add(category)
        await session.commit()
        await session.refresh(category)

        return category

    @staticmethod
    async def delete_category(
        session: AsyncSession,
        category: Category,
    ) -> None:
        """
        Delete a category.

        Args:
            session: Database session
            category: Category to delete
        """
        await session.delete(category)
        await session.commit()
