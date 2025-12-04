"""
FastAPI backend for pyplots platform.

AI-powered Python plotting examples that work with YOUR data.
"""

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


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
    """
    Manage application lifecycle.

    Handles startup and shutdown events for the application.
    """
    # Startup
    logger.info("Starting pyplots API...")
    yield
    # Shutdown
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
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:8000",  # API dev server
        "http://localhost:8080",
        "https://pyplots.ai",  # Production (future)
        "https://*.pyplots.ai",  # Subdomains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint - Hello World.
    """
    return {"message": "Welcome to pyplots API", "version": "0.1.0", "docs": "/docs", "health": "/health"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint for Cloud Run.
    """
    return JSONResponse(content={"status": "healthy", "service": "pyplots-api", "version": "0.1.0"}, status_code=200)


# Simple hello endpoint
@app.get("/hello/{name}")
async def hello(name: str):
    """
    Simple hello endpoint for testing.
    """
    return {"message": f"Hello, {name}!", "service": "pyplots"}


# ============================================================================
# Spec and Image Endpoints
# ============================================================================


def list_spec_ids() -> list[str]:
    """
    List all available spec IDs from the specs directory.

    Returns:
        List of spec IDs (without .md extension)
    """
    if not SPECS_DIR.exists():
        return []

    excluded = {".template", "VERSIONING"}
    specs = []
    for f in SPECS_DIR.glob("*.md"):
        spec_id = f.stem
        if spec_id not in excluded:
            specs.append(spec_id)
    return sorted(specs)


def get_latest_images_for_spec(spec_id: str) -> list[dict]:
    """
    Get latest plot images for a spec from GCS.

    Args:
        spec_id: The specification ID

    Returns:
        List of dicts with library name and image URL
    """
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
                    # Path: plots/{spec_id}/{library}/{variant}/v{timestamp}.png
                    library = parts[2]
                    # Keep the newest (lexicographically highest timestamp)
                    if library not in library_images or blob.name > library_images[library]:
                        library_images[library] = blob.name

        return [
            {"library": lib, "url": f"https://storage.googleapis.com/{GCS_BUCKET}/{path}"}
            for lib, path in sorted(library_images.items())
        ]
    except Exception as e:
        logger.error(f"Error fetching images from GCS: {e}")
        return []


@app.get("/specs")
async def get_specs():
    """
    Get list of all available plot specifications.

    Returns:
        List of spec IDs
    """
    specs = list_spec_ids()
    return {"specs": specs}


@app.get("/specs/{spec_id}/images")
async def get_spec_images(spec_id: str):
    """
    Get latest plot images for a specification across all libraries.

    Args:
        spec_id: The specification ID (e.g., 'scatter-basic')

    Returns:
        Spec ID and list of images with library names and URLs
    """
    # Verify spec exists
    available_specs = list_spec_ids()
    if spec_id not in available_specs:
        raise HTTPException(status_code=404, detail=f"Spec '{spec_id}' not found")

    images = get_latest_images_for_spec(spec_id)
    return {"spec_id": spec_id, "images": images}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
