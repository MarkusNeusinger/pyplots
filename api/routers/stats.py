"""Stats endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.cache import cache_key, get_cache, set_cache
from api.dependencies import optional_db
from api.schemas import StatsResponse
from core.constants import LIBRARIES_METADATA
from core.database import LibraryRepository, SpecRepository


router = APIRouter(tags=["stats"])


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: AsyncSession | None = Depends(optional_db)):
    """
    Get platform statistics.

    Returns counts of specs, implementations (plots), and libraries.
    """
    if db is None:
        return StatsResponse(specs=0, plots=0, libraries=len(LIBRARIES_METADATA))

    key = cache_key("stats")
    cached = get_cache(key)
    if cached:
        return cached

    spec_repo = SpecRepository(db)
    lib_repo = LibraryRepository(db)

    specs = await spec_repo.get_all()
    libraries = await lib_repo.get_all()

    # Count specs with at least one implementation
    specs_with_impls = [s for s in specs if s.impls]
    # Count total implementations
    total_impls = sum(len(s.impls) for s in specs)

    result = StatsResponse(specs=len(specs_with_impls), plots=total_impls, libraries=len(libraries))
    set_cache(key, result)
    return result
