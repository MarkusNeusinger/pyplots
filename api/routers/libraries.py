"""Library endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.cache import cache_key, get_cached, set_cached
from core.database import LIBRARIES_SEED, LibraryRepository, SpecRepository, get_db, is_db_configured


router = APIRouter(tags=["libraries"])


@router.get("/libraries")
async def get_libraries(db: AsyncSession = Depends(get_db)):
    """
    Get list of all supported plotting libraries.

    Returns library information including name, version, documentation URL, and description.
    """
    if not is_db_configured():
        return {"libraries": LIBRARIES_SEED}

    key = cache_key("libraries")
    cached = get_cached(key)
    if cached:
        return cached

    repo = LibraryRepository(db)
    libraries = await repo.get_all()

    result = {
        "libraries": [
            {
                "id": lib.id,
                "name": lib.name,
                "version": lib.version,
                "documentation_url": lib.documentation_url,
                "description": lib.description,
            }
            for lib in libraries
        ]
    }
    set_cached(key, result)
    return result


@router.get("/libraries/{library_id}/images")
async def get_library_images(library_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get all plot images for a specific library across all specs.

    Args:
        library_id: The library ID (e.g., 'matplotlib', 'seaborn')

    Returns:
        List of images with spec_id, preview_url, thumb, and html
    """
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    # Validate library_id
    valid_libraries = [lib["id"] for lib in LIBRARIES_SEED]
    if library_id not in valid_libraries:
        raise HTTPException(status_code=404, detail=f"Library '{library_id}' not found")

    key = cache_key("lib_images", library_id)
    cached = get_cached(key)
    if cached:
        return cached

    repo = SpecRepository(db)
    specs = await repo.get_all()

    images = []
    for spec in specs:
        for impl in spec.impls:
            if impl.library_id == library_id and impl.preview_url:
                images.append(
                    {
                        "spec_id": spec.id,
                        "library": impl.library_id,
                        "url": impl.preview_url,
                        "thumb": impl.preview_thumb,
                        "html": impl.preview_html,
                        "code": impl.code,
                    }
                )

    result = {"library": library_id, "images": images}
    set_cached(key, result)
    return result
