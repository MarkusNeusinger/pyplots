"""OG Image endpoints for branded social media preview images."""

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.cache import cache_key, get_cache, set_cache
from api.dependencies import optional_db
from core.database import SpecRepository
from core.images import create_branded_og_image, create_og_collage


router = APIRouter(prefix="/og", tags=["og-images"])

# Cache TTL for generated images (1 hour)
OG_IMAGE_CACHE_TTL = 3600


async def _fetch_image(url: str) -> bytes:
    """Fetch an image from a URL."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.content


@router.get("/{spec_id}/{library}.png")
async def get_branded_impl_image(
    spec_id: str, library: str, db: AsyncSession | None = Depends(optional_db)
) -> Response:
    """Get a branded OG image for an implementation.

    Returns a 1200x630 PNG with pyplots.ai header and the plot image.
    """
    # Check cache first
    key = cache_key("og", spec_id, library)
    cached = get_cache(key)
    if cached:
        return Response(content=cached, media_type="image/png")

    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    repo = SpecRepository(db)
    spec = await repo.get_by_id(spec_id)
    if not spec:
        raise HTTPException(status_code=404, detail="Spec not found")

    # Find the implementation
    impl = next((i for i in spec.impls if i.library_id == library), None)
    if not impl or not impl.preview_url:
        raise HTTPException(status_code=404, detail="Implementation not found")

    try:
        # Fetch the original plot image
        image_bytes = await _fetch_image(impl.preview_url)

        # Create branded image
        branded_bytes = create_branded_og_image(image_bytes, spec_id=spec_id, library=library)

        # Cache the result
        set_cache(key, branded_bytes, ttl=OG_IMAGE_CACHE_TTL)

        return Response(content=branded_bytes, media_type="image/png")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch image: {e}") from e


@router.get("/{spec_id}.png")
async def get_spec_collage_image(spec_id: str, db: AsyncSession | None = Depends(optional_db)) -> Response:
    """Get a collage OG image for a spec (showing top 6 implementations by quality).

    Returns a 1200x630 PNG with pyplots.ai branding and a 2x3 grid of implementations,
    sorted by quality_score descending.
    """
    # Check cache first
    key = cache_key("og", spec_id, "collage")
    cached = get_cache(key)
    if cached:
        return Response(content=cached, media_type="image/png")

    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    repo = SpecRepository(db)
    spec = await repo.get_by_id(spec_id)
    if not spec:
        raise HTTPException(status_code=404, detail="Spec not found")

    # Get implementations with preview images
    impls_with_preview = [i for i in spec.impls if i.preview_url]
    if not impls_with_preview:
        raise HTTPException(status_code=404, detail="No implementations with previews")

    # Sort by quality_score (descending) and take top 6 for 2x3 grid
    sorted_impls = sorted(
        impls_with_preview, key=lambda i: i.quality_score if i.quality_score is not None else 0, reverse=True
    )
    selected_impls = sorted_impls[:6]

    try:
        # Fetch all images
        images: list[bytes] = []
        labels: list[str] = []
        for impl in selected_impls:
            image_bytes = await _fetch_image(impl.preview_url)
            images.append(image_bytes)
            # Label format: "spec_id · library" like in og-image.png
            labels.append(f"{spec_id} · {impl.library_id}")

        # Create collage
        collage_bytes = create_og_collage(images, spec_id=spec_id, labels=labels)

        # Cache the result
        set_cache(key, collage_bytes, ttl=OG_IMAGE_CACHE_TTL)

        return Response(content=collage_bytes, media_type="image/png")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch images: {e}") from e
