"""
Repository classes for database access.

Provides abstraction layer between API and database models.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database.models import Impl, Library, Spec


# =============================================================================
# Field Validation - Allowed fields for update operations
# =============================================================================
# These sets define which fields can be updated via the update() methods.
# This prevents accidental modification of internal fields like 'id'.

SPEC_UPDATABLE_FIELDS = frozenset(
    {"title", "description", "applications", "data", "notes", "created", "updated", "issue", "suggested", "tags"}
)

LIBRARY_UPDATABLE_FIELDS = frozenset({"name", "version", "documentation_url", "description"})

IMPL_UPDATABLE_FIELDS = frozenset(
    {
        "code",
        "preview_url",
        "preview_thumb",
        "preview_html",
        "python_version",
        "library_version",
        "tested",
        "quality_score",
        "generated_at",
        "updated",
        "generated_by",
        "issue",
        "workflow_run",
        "review_strengths",
        "review_weaknesses",
        "review_image_description",
        "review_criteria_checklist",
        "review_verdict",
        "impl_tags",
    }
)


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
        result = await self.session.execute(select(Spec).options(selectinload(Spec.impls)))
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
            select(Spec).where(Spec.id == spec_id).options(selectinload(Spec.impls).selectinload(Impl.library))
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
        # Build filter: search for any tag value in the JSON structure
        # Works with both PostgreSQL and SQLite
        from sqlalchemy import String, cast, or_

        # Convert tags JSON to string and search for each tag
        filters = []
        for tag in tags:
            filters.append(cast(Spec.tags, String).contains(f'"{tag}"'))

        result = await self.session.execute(select(Spec).where(or_(*filters)).options(selectinload(Spec.impls)))
        return list(result.scalars().all())

    async def create(self, spec_data: dict) -> Spec:
        """
        Create a new spec.

        Args:
            spec_data: Dict with spec attributes (id, title, description, etc.)

        Returns:
            Created Spec object

        Example:
            spec = await repo.create({
                "id": "scatter-basic",
                "title": "Basic Scatter Plot",
                "description": "A simple scatter plot...",
                "applications": ["Statistics", "Data Analysis"],
                "tags": {"plot_type": ["scatter"], "domain": ["statistics"]}
            })
        """
        spec = Spec(**spec_data)
        self.session.add(spec)
        await self.session.commit()
        await self.session.refresh(spec)
        return spec

    async def update(self, spec_id: str, spec_data: dict) -> Optional[Spec]:
        """
        Update an existing spec.

        Args:
            spec_id: The specification ID
            spec_data: Dict with fields to update (only allowed fields are updated)

        Returns:
            Updated Spec object or None if not found

        Example:
            spec = await repo.update("scatter-basic", {
                "title": "Updated Title",
                "description": "New description"
            })
        """
        spec = await self.get_by_id(spec_id)
        if not spec:
            return None

        # Only update allowed fields to prevent modification of internal fields
        for key, value in spec_data.items():
            if key in SPEC_UPDATABLE_FIELDS:
                setattr(spec, key, value)

        await self.session.commit()
        await self.session.refresh(spec)
        return spec

    async def delete(self, spec_id: str) -> bool:
        """
        Delete a spec and all its implementations (cascade).

        Args:
            spec_id: The specification ID

        Returns:
            True if deleted, False if not found
        """
        spec = await self.get_by_id(spec_id)
        if not spec:
            return False

        await self.session.delete(spec)
        await self.session.commit()
        return True

    async def upsert(self, spec_data: dict) -> Spec:
        """
        Create or update a spec atomically using INSERT ... ON CONFLICT.

        Args:
            spec_data: Dict with spec attributes including 'id'

        Returns:
            Created or updated Spec object

        Example:
            spec = await repo.upsert({
                "id": "scatter-basic",
                "title": "Basic Scatter Plot",
                ...
            })
        """
        spec_id = spec_data.get("id")
        if not spec_id:
            raise ValueError("spec_data must include 'id' field")

        # Build update set with only allowed fields
        update_set = {k: v for k, v in spec_data.items() if k in SPEC_UPDATABLE_FIELDS}

        # Atomic upsert using PostgreSQL INSERT ... ON CONFLICT
        stmt = (
            insert(Spec)
            .values(**spec_data)
            .on_conflict_do_update(index_elements=["id"], set_=update_set)
            .returning(Spec)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()
        spec = result.scalar_one()
        await self.session.refresh(spec)
        return spec


class LibraryRepository:
    """Repository for Library operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Library]:
        """
        Get all libraries.

        Returns:
            List of Library objects
        """
        query = select(Library).order_by(Library.name)
        result = await self.session.execute(query)
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

    async def create(self, library_data: dict) -> Library:
        """
        Create a new library.

        Args:
            library_data: Dict with library attributes (id, name, version, etc.)

        Returns:
            Created Library object
        """
        library = Library(**library_data)
        self.session.add(library)
        await self.session.commit()
        await self.session.refresh(library)
        return library

    async def update(self, library_id: str, library_data: dict) -> Optional[Library]:
        """
        Update an existing library.

        Args:
            library_id: The library ID
            library_data: Dict with fields to update (only allowed fields are updated)

        Returns:
            Updated Library object or None if not found
        """
        library = await self.get_by_id(library_id)
        if not library:
            return None

        # Only update allowed fields to prevent modification of internal fields
        for key, value in library_data.items():
            if key in LIBRARY_UPDATABLE_FIELDS:
                setattr(library, key, value)

        await self.session.commit()
        await self.session.refresh(library)
        return library

    async def delete(self, library_id: str) -> bool:
        """
        Delete a library (cascade deletes implementations).

        Args:
            library_id: The library ID

        Returns:
            True if deleted, False if not found
        """
        library = await self.get_by_id(library_id)
        if not library:
            return False

        await self.session.delete(library)
        await self.session.commit()
        return True

    async def upsert(self, library_data: dict) -> Library:
        """
        Create or update a library atomically using INSERT ... ON CONFLICT.

        Args:
            library_data: Dict with library attributes including 'id'

        Returns:
            Created or updated Library object
        """
        library_id = library_data.get("id")
        if not library_id:
            raise ValueError("library_data must include 'id' field")

        # Build update set with only allowed fields
        update_set = {k: v for k, v in library_data.items() if k in LIBRARY_UPDATABLE_FIELDS}

        # Atomic upsert using PostgreSQL INSERT ... ON CONFLICT
        stmt = (
            insert(Library)
            .values(**library_data)
            .on_conflict_do_update(index_elements=["id"], set_=update_set)
            .returning(Library)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()
        library = result.scalar_one()
        await self.session.refresh(library)
        return library


class ImplRepository:
    """Repository for Impl operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_spec(self, spec_id: str) -> list[Impl]:
        """
        Get all implementations for a spec.

        Args:
            spec_id: The specification ID

        Returns:
            List of Impl objects
        """
        result = await self.session.execute(
            select(Impl).where(Impl.spec_id == spec_id).options(selectinload(Impl.library)).order_by(Impl.library_id)
        )
        return list(result.scalars().all())

    async def get_by_library(self, library_id: str) -> list[Impl]:
        """
        Get all implementations for a library.

        Args:
            library_id: The library ID

        Returns:
            List of Impl objects
        """
        result = await self.session.execute(
            select(Impl).where(Impl.library_id == library_id).options(selectinload(Impl.spec)).order_by(Impl.spec_id)
        )
        return list(result.scalars().all())

    async def get_by_spec_and_library(self, spec_id: str, library_id: str) -> Optional[Impl]:
        """
        Get a specific implementation.

        Args:
            spec_id: The specification ID
            library_id: The library ID

        Returns:
            Impl object or None if not found
        """
        result = await self.session.execute(select(Impl).where(Impl.spec_id == spec_id, Impl.library_id == library_id))
        return result.scalar_one_or_none()

    async def create(self, impl_data: dict) -> Impl:
        """
        Create a new implementation.

        Args:
            impl_data: Dict with implementation attributes

        Returns:
            Created Impl object

        Example:
            impl = await repo.create({
                "spec_id": "scatter-basic",
                "library_id": "matplotlib",
                "code": "import matplotlib.pyplot as plt...",
                "preview_url": "https://...",
                "quality_score": 92
            })
        """
        impl = Impl(**impl_data)
        self.session.add(impl)
        await self.session.commit()
        await self.session.refresh(impl)
        return impl

    async def update(self, impl_id: str, impl_data: dict) -> Optional[Impl]:
        """
        Update an existing implementation.

        Args:
            impl_id: The implementation ID (UUID)
            impl_data: Dict with fields to update (only allowed fields are updated)

        Returns:
            Updated Impl object or None if not found
        """
        result = await self.session.execute(select(Impl).where(Impl.id == impl_id))
        impl = result.scalar_one_or_none()
        if not impl:
            return None

        # Only update allowed fields to prevent modification of internal fields
        for key, value in impl_data.items():
            if key in IMPL_UPDATABLE_FIELDS:
                setattr(impl, key, value)

        await self.session.commit()
        await self.session.refresh(impl)
        return impl

    async def delete(self, impl_id: str) -> bool:
        """
        Delete an implementation.

        Args:
            impl_id: The implementation ID (UUID)

        Returns:
            True if deleted, False if not found
        """
        result = await self.session.execute(select(Impl).where(Impl.id == impl_id))
        impl = result.scalar_one_or_none()
        if not impl:
            return False

        await self.session.delete(impl)
        await self.session.commit()
        return True

    async def upsert(self, spec_id: str, library_id: str, impl_data: dict) -> Impl:
        """
        Create or update an implementation atomically using INSERT ... ON CONFLICT.

        Args:
            spec_id: The specification ID
            library_id: The library ID
            impl_data: Dict with implementation attributes

        Returns:
            Created or updated Impl object

        Example:
            impl = await repo.upsert("scatter-basic", "matplotlib", {
                "code": "import matplotlib.pyplot as plt...",
                "quality_score": 95
            })
        """
        # Build the full data with spec_id and library_id
        full_data = {**impl_data, "spec_id": spec_id, "library_id": library_id}

        # Build update set with only allowed fields
        update_set = {k: v for k, v in impl_data.items() if k in IMPL_UPDATABLE_FIELDS}

        # Atomic upsert using PostgreSQL INSERT ... ON CONFLICT on the unique constraint
        stmt = (
            insert(Impl)
            .values(**full_data)
            .on_conflict_do_update(constraint="uq_impl", set_=update_set)
            .returning(Impl)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()
        impl = result.scalar_one()
        await self.session.refresh(impl)
        return impl
