"""Stats endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.cache import cache_key, get_cache, get_or_set_cache
from api.dependencies import optional_db
from api.schemas import StatsResponse
from core.config import settings
from core.constants import LIBRARIES_METADATA
from core.database import LibraryRepository, SpecRepository
from core.database.connection import get_db_context


router = APIRouter(tags=["stats"])


async def _refresh_stats() -> StatsResponse:
    """Standalone factory for background refresh (creates own DB session)."""
    # Try to derive from already-cached endpoint responses
    specs_cached = get_cache(cache_key("specs_list"))
    libs_cached = get_cache(cache_key("libraries"))

    if specs_cached is not None and libs_cached is not None:
        return StatsResponse(
            specs=len(specs_cached),
            plots=sum(item.library_count for item in specs_cached),
            libraries=len(libs_cached["libraries"]),
        )

    async with get_db_context() as db:
        spec_repo = SpecRepository(db)
        lib_repo = LibraryRepository(db)
        specs = await spec_repo.get_all()
        libraries = await lib_repo.get_all()

    specs_with_impls = [s for s in specs if s.impls]
    total_impls = sum(len(s.impls) for s in specs)
    return StatsResponse(specs=len(specs_with_impls), plots=total_impls, libraries=len(libraries))


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: AsyncSession | None = Depends(optional_db)):
    """
    Get platform statistics.

    Returns counts of specs, implementations (plots), and libraries.
    """
    if db is None:
        return StatsResponse(specs=0, plots=0, libraries=len(LIBRARIES_METADATA))

    async def _fetch() -> StatsResponse:
        # Try to derive from already-cached endpoint responses
        specs_cached = get_cache(cache_key("specs_list"))
        libs_cached = get_cache(cache_key("libraries"))

        if specs_cached is not None and libs_cached is not None:
            return StatsResponse(
                specs=len(specs_cached),
                plots=sum(item.library_count for item in specs_cached),
                libraries=len(libs_cached["libraries"]),
            )

        # Fallback: DB query (only on cold start if /stats arrives before /specs)
        spec_repo = SpecRepository(db)
        lib_repo = LibraryRepository(db)
        specs = await spec_repo.get_all()
        libraries = await lib_repo.get_all()

        specs_with_impls = [s for s in specs if s.impls]
        total_impls = sum(len(s.impls) for s in specs)
        return StatsResponse(specs=len(specs_with_impls), plots=total_impls, libraries=len(libraries))

    return await get_or_set_cache(
        cache_key("stats"),
        _fetch,
        refresh_after=settings.cache_refresh_after,
        refresh_factory=_refresh_stats,
    )
