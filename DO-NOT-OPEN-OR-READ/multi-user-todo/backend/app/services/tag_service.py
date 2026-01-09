"""Tag service for tag-related business logic."""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.tag import Tag
from app.utils.errors import ConflictException, NotFoundException


class TagService:
    """Service class for tag operations."""

    @staticmethod
    async def create_tag(
        session: AsyncSession,
        user_id: UUID,
        name: str,
    ) -> Tag:
        """
        Create a new tag.

        Args:
            session: Database session
            user_id: User ID
            name: Tag name

        Returns:
            Created tag

        Raises:
            ConflictException: If tag name already exists for user
        """
        # Check if tag name already exists for this user
        statement = select(Tag).where(
            Tag.user_id == user_id,
            Tag.name == name,
        )
        result = await session.exec(statement)
        if result.first():
            raise ConflictException(
                f"Tag '{name}' already exists",
                details={"field": "name"},
            )

        tag = Tag(
            id=uuid4(),
            name=name,
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
        )

        session.add(tag)
        await session.commit()
        await session.refresh(tag)

        return tag

    @staticmethod
    async def get_user_tags(
        session: AsyncSession,
        user_id: UUID,
    ) -> list[Tag]:
        """
        Get all tags for a user.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            List of tags
        """
        statement = select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
        result = await session.exec(statement)
        return result.all()

    @staticmethod
    async def get_tag_by_id(
        session: AsyncSession,
        tag_id: UUID,
        user_id: UUID,
    ) -> Optional[Tag]:
        """
        Get a specific tag by ID (must belong to user).

        Args:
            session: Database session
            tag_id: Tag ID
            user_id: User ID

        Returns:
            Tag if found, None otherwise
        """
        statement = select(Tag).where(
            Tag.id == tag_id,
            Tag.user_id == user_id,
        )
        result = await session.exec(statement)
        return result.first()

    @staticmethod
    async def update_tag(
        session: AsyncSession,
        tag: Tag,
        name: str,
    ) -> Tag:
        """
        Update a tag.

        Args:
            session: Database session
            tag: Tag to update
            name: New name

        Returns:
            Updated tag

        Raises:
            ConflictException: If new name already exists for user
        """
        # Check if new name conflicts with another tag
        statement = select(Tag).where(
            Tag.user_id == tag.user_id,
            Tag.name == name,
            Tag.id != tag.id,
        )
        result = await session.exec(statement)
        if result.first():
            raise ConflictException(
                f"Tag '{name}' already exists",
                details={"field": "name"},
            )

        tag.name = name

        session.add(tag)
        await session.commit()
        await session.refresh(tag)

        return tag

    @staticmethod
    async def delete_tag(
        session: AsyncSession,
        tag: Tag,
    ) -> None:
        """
        Delete a tag.

        Args:
            session: Database session
            tag: Tag to delete
        """
        await session.delete(tag)
        await session.commit()
