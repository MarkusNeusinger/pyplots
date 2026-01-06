"""
FastAPI backend for pyplots platform.

AI-powered Python plotting examples that work with YOUR data.
"""

# Load .env file FIRST, before any other imports that might read env vars
from dotenv import load_dotenv  # noqa: E402, I001

load_dotenv()

import logging  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI, HTTPException, Request, Response  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from starlette.middleware.gzip import GZipMiddleware  # noqa: E402

from api.exceptions import (  # noqa: E402
    PyplotsException,
    generic_exception_handler,
    http_exception_handler,
    pyplots_exception_handler,
)
from api.routers import (  # noqa: E402
    download_router,
    health_router,
    libraries_router,
    og_images_router,
    plots_router,
    proxy_router,
    seo_router,
    specs_router,
    stats_router,
)
from core.database import close_db, init_db, is_db_configured  # noqa: E402


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
    description="Backend API for pyplots.ai - Python plotting gallery across 9 libraries",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Register exception handlers
app.add_exception_handler(PyplotsException, pyplots_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Enable GZip compression for responses > 500 bytes
# This significantly reduces payload size for JSON API responses
# (e.g., /plots/filter: 301KB -> ~40KB with gzip)
# Note: GZip must be added before CORS so compression happens before CORS headers are added
app.add_middleware(GZipMiddleware, minimum_size=500)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pyplots.ai"],
    allow_origin_regex=r"http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add cache headers middleware
@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    """Add Cache-Control headers to API responses for better browser caching."""
    response: Response = await call_next(request)

    # Skip for non-GET requests or error responses
    if request.method != "GET" or response.status_code >= 400:
        return response

    path = request.url.path

    # Static data that rarely changes (5 min cache, stale-while-revalidate for 1 hour)
    if path in ("/libraries", "/stats"):
        response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=3600"
    # Specs list - moderate caching (2 min cache)
    elif path == "/specs":
        response.headers["Cache-Control"] = "public, max-age=120, stale-while-revalidate=600"
    # Filter endpoint - short cache (30 sec) with stale-while-revalidate
    elif path == "/plots/filter":
        response.headers["Cache-Control"] = "public, max-age=30, stale-while-revalidate=300"
    # Individual spec details
    elif path.startswith("/specs/"):
        response.headers["Cache-Control"] = "public, max-age=120, stale-while-revalidate=600"

    return response


# Register routers
app.include_router(health_router)
app.include_router(stats_router)
app.include_router(specs_router)
app.include_router(libraries_router)
app.include_router(plots_router)
app.include_router(download_router)
app.include_router(seo_router)
app.include_router(og_images_router)
app.include_router(proxy_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
