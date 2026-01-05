"""Library endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.cache import cache_key, get_cache, set_cache
from api.dependencies import optional_db, require_db
from api.exceptions import raise_not_found
from core.constants import LIBRARIES_METADATA, SUPPORTED_LIBRARIES
from core.database import LibraryRepository, SpecRepository
from core.utils import strip_noqa_comments


router = APIRouter(tags=["libraries"])


@router.get("/libraries")
async def get_libraries(db: AsyncSession | None = Depends(optional_db)):
    """
    Get list of all supported plotting libraries.

    Returns library information including name, version, documentation URL, and description.
    """
    if db is None:
        return {"libraries": LIBRARIES_METADATA}

    key = cache_key("libraries")
    cached = get_cache(key)
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
    set_cache(key, result)
    return result


@router.get("/libraries/{library_id}/images")
async def get_library_images(library_id: str, db: AsyncSession = Depends(require_db)):
    """
    Get all plot images for a specific library across all specs.

    Args:
        library_id: The library ID (e.g., 'matplotlib', 'seaborn')

    Returns:
        List of images with spec_id, preview_url, thumb, and html
    """

    # Validate library_id
    if library_id not in SUPPORTED_LIBRARIES:
        raise_not_found("Library", library_id)

    key = cache_key("lib_images", library_id)
    cached = get_cache(key)
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
                        "code": strip_noqa_comments(impl.code),
                    }
                )

    result = {"library": library_id, "images": images}
    set_cache(key, result)
    return result
