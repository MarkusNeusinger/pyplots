"""
FastAPI backend for pyplots platform.

AI-powered Python plotting examples that work with YOUR data.
"""

# Load .env file FIRST, before any other imports that might read env vars
from dotenv import load_dotenv  # noqa: E402, I001

load_dotenv()

import logging  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402
from typing import Optional  # noqa: E402

import httpx  # noqa: E402

from fastapi import Depends, FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import JSONResponse, Response  # noqa: E402
from pydantic import BaseModel  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: E402

from core.database import (  # noqa: E402
    LIBRARIES_SEED,
    LibraryRepository,
    SpecRepository,
    close_db,
    get_db,
    init_db,
    is_db_configured,
)


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    logger.info("Starting pyplots API...")

    # Initialize database connection
    if is_db_configured():
        try:
            await init_db()
            logger.info("Database connection initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

    yield

    # Cleanup database connection
    logger.info("Shutting down pyplots API...")
    await close_db()


# Create FastAPI application
app = FastAPI(
    title="pyplots API",
    description="AI-powered Python plotting examples that work with YOUR data",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pyplots.ai"],
    allow_origin_regex=r"http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Health & Info Endpoints
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to pyplots API", "version": "0.1.0", "docs": "/docs", "health": "/health"}


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return JSONResponse(content={"status": "healthy", "service": "pyplots-api", "version": "0.1.0"}, status_code=200)


@app.get("/hello/{name}")
async def hello(name: str):
    """Simple hello endpoint for testing."""
    return {"message": f"Hello, {name}!", "service": "pyplots"}


# ============================================================================
# Pydantic Models
# ============================================================================


class ImplementationResponse(BaseModel):
    """Implementation details."""

    library_id: str
    library_name: str
    preview_url: Optional[str] = None
    preview_thumb: Optional[str] = None
    preview_html: Optional[str] = None
    quality_score: Optional[float] = None
    code: Optional[str] = None
    generated_at: Optional[str] = None
    generated_by: Optional[str] = None
    python_version: Optional[str] = None
    library_version: Optional[str] = None


class SpecDetailResponse(BaseModel):
    """Detailed spec response with implementations."""

    id: str
    title: str
    description: Optional[str] = None
    applications: list[str] = []
    data: list[str] = []
    notes: list[str] = []
    tags: Optional[dict] = None
    issue: Optional[int] = None
    suggested: Optional[str] = None
    implementations: list[ImplementationResponse] = []


class SpecListItem(BaseModel):
    """Spec list item with summary info."""

    id: str
    title: str
    description: Optional[str] = None
    tags: Optional[dict] = None
    library_count: int = 0


# ============================================================================
# Spec Endpoints
# ============================================================================


@app.get("/specs", response_model=list[SpecListItem])
async def get_specs(db: AsyncSession = Depends(get_db)):
    """
    Get list of all specs with metadata.

    Returns only specs that have at least one implementation.
    """
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    repo = SpecRepository(db)
    specs = await repo.get_all()

    # Only return specs with at least one implementation
    return [
        SpecListItem(
            id=spec.id, title=spec.title, description=spec.description, tags=spec.tags, library_count=len(spec.impls)
        )
        for spec in specs
        if spec.impls  # Filter: only specs with implementations
    ]


@app.get("/specs/{spec_id}", response_model=SpecDetailResponse)
async def get_spec(spec_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get detailed spec information including all implementations.

    Args:
        spec_id: The specification ID (e.g., 'scatter-basic')

    Returns:
        Full spec details with all library implementations and preview URLs
    """
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    repo = SpecRepository(db)
    spec = await repo.get_by_id(spec_id)

    if not spec:
        raise HTTPException(status_code=404, detail=f"Spec '{spec_id}' not found")

    # Only return spec if it has implementations
    if not spec.impls:
        raise HTTPException(status_code=404, detail=f"Spec '{spec_id}' has no implementations")

    impls = [
        ImplementationResponse(
            library_id=impl.library_id,
            library_name=impl.library.name if impl.library else impl.library_id,
            preview_url=impl.preview_url,
            preview_thumb=impl.preview_thumb,
            preview_html=impl.preview_html,
            quality_score=impl.quality_score,
            code=impl.code,
            generated_at=impl.generated_at.isoformat() if impl.generated_at else None,
            generated_by=impl.generated_by,
            python_version=impl.python_version,
            library_version=impl.library_version,
        )
        for impl in spec.impls
    ]

    return SpecDetailResponse(
        id=spec.id,
        title=spec.title,
        description=spec.description,
        applications=spec.applications or [],
        data=spec.data or [],
        notes=spec.notes or [],
        tags=spec.tags,
        issue=spec.issue,
        suggested=spec.suggested,
        implementations=impls,
    )


@app.get("/specs/{spec_id}/images")
async def get_spec_images(spec_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get plot images for a specification across all libraries.

    Returns preview_url, preview_thumb, and preview_html from database.
    """
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    repo = SpecRepository(db)
    spec = await repo.get_by_id(spec_id)

    if not spec:
        raise HTTPException(status_code=404, detail=f"Spec '{spec_id}' not found")

    if not spec.impls:
        raise HTTPException(status_code=404, detail=f"Spec '{spec_id}' has no implementations")

    images = [
        {"library": impl.library_id, "url": impl.preview_url, "thumb": impl.preview_thumb, "html": impl.preview_html}
        for impl in spec.impls
        if impl.preview_url  # Only include if there's a preview
    ]

    return {"spec_id": spec_id, "images": images}


# ============================================================================
# Library Endpoints
# ============================================================================


@app.get("/libraries")
async def get_libraries(db: AsyncSession = Depends(get_db)):
    """
    Get list of all supported plotting libraries.

    Returns library information including name, version, and documentation URL.
    """
    if not is_db_configured():
        return {"libraries": LIBRARIES_SEED}

    repo = LibraryRepository(db)
    libraries = await repo.get_all()

    return {
        "libraries": [
            {"id": lib.id, "name": lib.name, "version": lib.version, "documentation_url": lib.documentation_url}
            for lib in libraries
        ]
    }


# ============================================================================
# Download Proxy Endpoints
# ============================================================================


@app.get("/download/{spec_id}/{library}")
async def download_image(spec_id: str, library: str, db: AsyncSession = Depends(get_db)):
    """
    Proxy download for plot images to avoid CORS issues.

    Returns the image as a downloadable file.
    """
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

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
            raise HTTPException(status_code=502, detail=f"Failed to fetch image: {e}")

    # Return as downloadable file
    filename = f"{spec_id}-{library}.png"
    return Response(
        content=response.content,
        media_type="image/png",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
