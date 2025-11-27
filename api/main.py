"""
FastAPI backend for pyplots platform.

AI-powered Python plotting examples that work with YOUR data.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
