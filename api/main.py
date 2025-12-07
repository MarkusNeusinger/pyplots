"""
FastAPI backend for pyplots platform.

AI-powered Python plotting examples that work with YOUR data.
"""

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LIBRARIES_SEED, LibraryRepository, SpecRepository, get_db, is_db_configured


# Try to import GCS client (optional)
try:
    from google.cloud import storage

    GCS_AVAILABLE = True
except ImportError:
    GCS_AVAILABLE = False

# Load .env file (works locally, ignored in Cloud Run if not present)
load_dotenv()

# Configuration
GCS_BUCKET = os.getenv("GCS_BUCKET", "pyplots-images")
BASE_DIR = Path(__file__).parent.parent
SPECS_DIR = BASE_DIR / "specs"


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    logger.info("Starting pyplots API...")
    yield
    logger.info("Shutting down pyplots API...")


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


class DataRequirement(BaseModel):
    """Data requirement for a spec."""

    name: str
    type: str
    description: str = ""


class ImplementationResponse(BaseModel):
    """Implementation details."""

    library_id: str
    library_name: str
    plot_function: str
    variant: str
    file_path: str
    preview_url: Optional[str] = None
    quality_score: Optional[float] = None


class SpecDetailResponse(BaseModel):
    """Detailed spec response with implementations."""

    id: str
    title: str
    description: Optional[str] = None
    data_requirements: list[DataRequirement] = []
    tags: list[str] = []
    implementations: list[ImplementationResponse] = []


class SpecListItem(BaseModel):
    """Spec list item with summary info."""

    id: str
    title: str
    description: Optional[str] = None
    tags: list[str] = []
    library_count: int = 0


# ============================================================================
# Helper Functions (Filesystem Fallback)
# ============================================================================


def list_spec_ids_from_filesystem() -> list[str]:
    """List spec IDs from filesystem (fallback when DB not configured)."""
    if not SPECS_DIR.exists():
        return []

    excluded = {".template", "VERSIONING"}
    return sorted([f.stem for f in SPECS_DIR.glob("*.md") if f.stem not in excluded])


def get_images_from_gcs(spec_id: str) -> list[dict]:
    """Get latest plot images for a spec from GCS."""
    if not GCS_AVAILABLE:
        logger.warning("GCS client not available - returning empty image list")
        return []

    try:
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET)
        prefix = f"plots/{spec_id}/"
        blobs = list(bucket.list_blobs(prefix=prefix))

        # Group by library, find newest image (excluding thumbnails)
        library_images: dict[str, str] = {}
        for blob in blobs:
            if blob.name.endswith(".png") and "_thumb" not in blob.name:
                parts = blob.name.split("/")
                if len(parts) >= 4:
                    library = parts[2]
                    if library not in library_images or blob.name > library_images[library]:
                        library_images[library] = blob.name

        return [
            {"library": lib, "url": f"https://storage.googleapis.com/{GCS_BUCKET}/{path}"}
            for lib, path in sorted(library_images.items())
        ]
    except Exception as e:
        logger.error(f"Error fetching images from GCS: {e}")
        return []


# ============================================================================
# Spec Endpoints
# ============================================================================


@app.get("/specs", response_model=list[SpecListItem])
async def get_specs(db: AsyncSession = Depends(get_db)):
    """
    Get list of all specs with metadata.

    Returns specs with title, description, tags, and implementation count.
    Falls back to filesystem if database is not configured.
    """
    if not is_db_configured():
        spec_ids = list_spec_ids_from_filesystem()
        return [SpecListItem(id=spec_id, title=spec_id) for spec_id in spec_ids]

    repo = SpecRepository(db)
    specs = await repo.get_all()

    return [
        SpecListItem(
            id=spec.id,
            title=spec.title,
            description=spec.description,
            tags=spec.tags or [],
            library_count=len(spec.implementations),
        )
        for spec in specs
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

    implementations = [
        ImplementationResponse(
            library_id=impl.library_id,
            library_name=impl.library.name if impl.library else impl.library_id,
            plot_function=impl.plot_function,
            variant=impl.variant,
            file_path=impl.file_path,
            preview_url=impl.preview_url,
            quality_score=impl.quality_score,
        )
        for impl in spec.implementations
    ]

    data_reqs = [
        DataRequirement(
            name=req.get("name", ""),
            type=req.get("type", ""),
            description=req.get("description", ""),
        )
        for req in (spec.data_requirements or [])
    ]

    return SpecDetailResponse(
        id=spec.id,
        title=spec.title,
        description=spec.description,
        data_requirements=data_reqs,
        tags=spec.tags or [],
        implementations=implementations,
    )


@app.get("/specs/{spec_id}/images")
async def get_spec_images(spec_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get latest plot images for a specification across all libraries.

    Fetches from GCS directly for the most up-to-date images.
    """
    # Verify spec exists in DB or filesystem
    if is_db_configured():
        repo = SpecRepository(db)
        spec = await repo.get_by_id(spec_id)
        if not spec:
            raise HTTPException(status_code=404, detail=f"Spec '{spec_id}' not found")
    else:
        available_specs = list_spec_ids_from_filesystem()
        if spec_id not in available_specs:
            raise HTTPException(status_code=404, detail=f"Spec '{spec_id}' not found")

    images = get_images_from_gcs(spec_id)
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
    libraries = await repo.get_all(active_only=True)

    return {
        "libraries": [
            {
                "id": lib.id,
                "name": lib.name,
                "version": lib.version,
                "documentation_url": lib.documentation_url,
            }
            for lib in libraries
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
