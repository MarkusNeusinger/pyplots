"""
FastAPI backend for pyplots platform.

AI-powered Python plotting examples that work with YOUR data.
"""

# Load .env file FIRST, before any other imports that might read env vars
from dotenv import load_dotenv  # noqa: E402, I001

load_dotenv()

import logging  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from api.routers import (  # noqa: E402
    download_router,
    health_router,
    libraries_router,
    plots_router,
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
    description="AI-powered Python plotting examples that work with YOUR data",
    version="0.2.0",
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

# Register routers
app.include_router(health_router)
app.include_router(stats_router)
app.include_router(specs_router)
app.include_router(libraries_router)
app.include_router(plots_router)
app.include_router(download_router)
app.include_router(seo_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
