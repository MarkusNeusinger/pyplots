"""
Repository classes for database access.

Provides abstraction layer between API and database models.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database.models import Implementation, Library, Spec


class SpecRepository:
    """Repository for Spec operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Spec]:
        """
        Get all specs with their implementations.

        Returns:
            List of Spec objects with implementations loaded
        """
        result = await self.session.execute(select(Spec).options(selectinload(Spec.implementations)))
        return list(result.scalars().all())

    async def get_by_id(self, spec_id: str) -> Optional[Spec]:
        """
        Get a spec by ID with all implementations and library info.

        Args:
            spec_id: The specification ID

        Returns:
            Spec object or None if not found
        """
        result = await self.session.execute(
            select(Spec)
            .where(Spec.id == spec_id)
            .options(selectinload(Spec.implementations).selectinload(Implementation.library))
        )
        return result.scalar_one_or_none()

    async def get_ids(self) -> list[str]:
        """
        Get all spec IDs.

        Returns:
            List of spec ID strings
        """
        result = await self.session.execute(select(Spec.id).order_by(Spec.id))
        return [row[0] for row in result.fetchall()]

    async def search_by_tags(self, tags: list[str]) -> list[Spec]:
        """
        Search specs by tags.

        Args:
            tags: List of tags to search for

        Returns:
            List of matching Spec objects
        """
        result = await self.session.execute(
            select(Spec).where(Spec.tags.overlap(tags)).options(selectinload(Spec.implementations))
        )
        return list(result.scalars().all())


class LibraryRepository:
    """Repository for Library operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, active_only: bool = True) -> list[Library]:
        """
        Get all libraries.

        Args:
            active_only: If True, only return active libraries

        Returns:
            List of Library objects
        """
        query = select(Library)
        if active_only:
            query = query.where(Library.active == True)  # noqa: E712
        result = await self.session.execute(query.order_by(Library.name))
        return list(result.scalars().all())

    async def get_by_id(self, library_id: str) -> Optional[Library]:
        """
        Get a library by ID.

        Args:
            library_id: The library ID

        Returns:
            Library object or None if not found
        """
        result = await self.session.execute(select(Library).where(Library.id == library_id))
        return result.scalar_one_or_none()


class ImplementationRepository:
    """Repository for Implementation operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_spec(self, spec_id: str) -> list[Implementation]:
        """
        Get all implementations for a spec.

        Args:
            spec_id: The specification ID

        Returns:
            List of Implementation objects
        """
        result = await self.session.execute(
            select(Implementation)
            .where(Implementation.spec_id == spec_id)
            .options(selectinload(Implementation.library))
            .order_by(Implementation.library_id)
        )
        return list(result.scalars().all())

    async def get_by_library(self, library_id: str) -> list[Implementation]:
        """
        Get all implementations for a library.

        Args:
            library_id: The library ID

        Returns:
            List of Implementation objects
        """
        result = await self.session.execute(
            select(Implementation)
            .where(Implementation.library_id == library_id)
            .options(selectinload(Implementation.spec))
            .order_by(Implementation.spec_id)
        )
        return list(result.scalars().all())

    async def get_by_spec_and_library(
        self, spec_id: str, library_id: str, variant: str = "default"
    ) -> Optional[Implementation]:
        """
        Get a specific implementation.

        Args:
            spec_id: The specification ID
            library_id: The library ID
            variant: The variant name (default: "default")

        Returns:
            Implementation object or None if not found
        """
        result = await self.session.execute(
            select(Implementation).where(
                Implementation.spec_id == spec_id,
                Implementation.library_id == library_id,
                Implementation.variant == variant,
            )
        )
        return result.scalar_one_or_none()
