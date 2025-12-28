"""Download proxy endpoint."""

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import require_db
from core.database import SpecRepository


router = APIRouter(tags=["download"])


@router.get("/download/{spec_id}/{library}")
async def download_image(spec_id: str, library: str, db: AsyncSession = Depends(require_db)):
    """
    Proxy download for plot images to avoid CORS issues.

    Returns the image as a downloadable file.
    """

    repo = SpecRepository(db)
    spec = await repo.get_by_id(spec_id)

    if not spec:
        raise HTTPException(status_code=404, detail=f"Spec '{spec_id}' not found")

    # Find the implementation for the requested library
    impl = next((i for i in spec.impls if i.library_id == library), None)
    if not impl or not impl.preview_url:
        raise HTTPException(status_code=404, detail=f"No image found for {spec_id}/{library}")

    # Fetch the image from GCS
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(impl.preview_url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Failed to fetch image: {e}") from e

    # Return as downloadable file
    filename = f"{spec_id}-{library}.png"
    return Response(
        content=response.content,
        media_type="image/png",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
