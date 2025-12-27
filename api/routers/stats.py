"""Stats endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.cache import cache_key, get_cached, set_cached
from api.schemas import StatsResponse
from core.database import LIBRARIES_SEED, LibraryRepository, SpecRepository, get_db, is_db_configured


router = APIRouter(tags=["stats"])


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    """
    Get platform statistics.

    Returns counts of specs, implementations (plots), and libraries.
    """
    if not is_db_configured():
        return StatsResponse(specs=0, plots=0, libraries=len(LIBRARIES_SEED))

    key = cache_key("stats")
    cached = get_cached(key)
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
    set_cached(key, result)
    return result
