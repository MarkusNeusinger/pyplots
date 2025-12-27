"""
FastAPI backend for pyplots platform.

AI-powered Python plotting examples that work with YOUR data.
"""

# Load .env file FIRST, before any other imports that might read env vars
from dotenv import load_dotenv  # noqa: E402, I001

load_dotenv()

import html  # noqa: E402
import logging  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402
from typing import Optional  # noqa: E402

import httpx  # noqa: E402
from cachetools import TTLCache  # noqa: E402
from fastapi import Depends, FastAPI, HTTPException, Request  # noqa: E402
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

# Cache for DB queries (1000 entries, 10 min TTL)
_cache: TTLCache = TTLCache(maxsize=1000, ttl=600)


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


# ============================================================================
# Health & Info Endpoints
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to pyplots API", "version": "0.2.0", "docs": "/docs", "health": "/health"}


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return JSONResponse(content={"status": "healthy", "service": "pyplots-api", "version": "0.2.0"}, status_code=200)


@app.get("/hello/{name}")
async def hello(name: str):
    """Simple hello endpoint for testing."""
    return {"message": f"Hello, {name}!", "service": "pyplots"}


# ============================================================================
# Stats Endpoint
# ============================================================================


@app.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """
    Get platform statistics.

    Returns counts of specs, implementations (plots), and libraries.
    """
    if not is_db_configured():
        return {"specs": 0, "plots": 0, "libraries": len(LIBRARIES_SEED)}

    cache_key = "stats"
    if cache_key in _cache:
        return _cache[cache_key]

    spec_repo = SpecRepository(db)
    lib_repo = LibraryRepository(db)

    specs = await spec_repo.get_all()
    libraries = await lib_repo.get_all()

    # Count specs with at least one implementation
    specs_with_impls = [s for s in specs if s.impls]
    # Count total implementations
    total_impls = sum(len(s.impls) for s in specs)

    result = {"specs": len(specs_with_impls), "plots": total_impls, "libraries": len(libraries)}
    _cache[cache_key] = result
    return result


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

    cache_key = "specs_list"
    if cache_key in _cache:
        return _cache[cache_key]

    repo = SpecRepository(db)
    specs = await repo.get_all()

    # Only return specs with at least one implementation
    result = [
        SpecListItem(
            id=spec.id, title=spec.title, description=spec.description, tags=spec.tags, library_count=len(spec.impls)
        )
        for spec in specs
        if spec.impls  # Filter: only specs with implementations
    ]
    _cache[cache_key] = result
    return result


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

    cache_key = f"spec:{spec_id}"
    if cache_key in _cache:
        return _cache[cache_key]

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

    result = SpecDetailResponse(
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
    _cache[cache_key] = result
    return result


@app.get("/specs/{spec_id}/images")
async def get_spec_images(spec_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get plot images for a specification across all libraries.

    Returns preview_url, preview_thumb, and preview_html from database.
    """
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    cache_key = f"spec_images:{spec_id}"
    if cache_key in _cache:
        return _cache[cache_key]

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

    result = {"spec_id": spec_id, "images": images}
    _cache[cache_key] = result
    return result


# ============================================================================
# Library Endpoints
# ============================================================================


@app.get("/libraries")
async def get_libraries(db: AsyncSession = Depends(get_db)):
    """
    Get list of all supported plotting libraries.

    Returns library information including name, version, documentation URL, and description.
    """
    if not is_db_configured():
        return {"libraries": LIBRARIES_SEED}

    cache_key = "libraries"
    if cache_key in _cache:
        return _cache[cache_key]

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
    _cache[cache_key] = result
    return result


@app.get("/libraries/{library_id}/images")
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

    cache_key = f"lib_images:{library_id}"
    if cache_key in _cache:
        return _cache[cache_key]

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
    _cache[cache_key] = result
    return result


# ============================================================================
# Filter Endpoint
# ============================================================================


class FilteredPlotsResponse(BaseModel):
    """Response for filtered plots with counts."""

    total: int
    images: list[dict]
    counts: dict  # Contextual counts (for AND additions)
    globalCounts: dict  # Global counts (for reference)
    orCounts: list[dict]  # Per-group counts for OR additions (with other filters applied)


@app.get("/plots/filter", response_model=FilteredPlotsResponse)
async def get_filtered_plots(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Get filtered plot images with counts for all filter categories.

    Filter logic:
    - Multiple values in same param: OR (lib=matplotlib,seaborn)
    - Multiple params with same name: AND (lib=matplotlib&lib=seaborn)
    - Different categories: AND (lib=matplotlib&plot=scatter)

    Query params (comma-separated for OR, multiple params for AND):
    - lib: Library filter (matplotlib, seaborn, etc.)
    - spec: Spec ID filter (scatter-basic, etc.)
    - plot: Plot type tag (scatter, bar, line, etc.)
    - data: Data type tag (numeric, categorical, etc.)
    - dom: Domain tag (statistics, finance, etc.)
    - feat: Features tag (basic, 3d, interactive, etc.)

    Returns:
        FilteredPlotsResponse with images, counts, and orCounts per group
    """
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")

    # Parse query params into filter groups
    # Each group is {category, values} - groups are AND-linked, values within are OR-linked
    filter_groups: list[dict] = []
    query_params = request.query_params.multi_items()

    for key, value in query_params:
        if key in ("lib", "spec", "plot", "data", "dom", "feat") and value:
            values = [v.strip() for v in value.split(",") if v.strip()]
            if values:
                filter_groups.append({"category": key, "values": values})

    # Build cache key from filter groups
    cache_parts = [f"{g['category']}={','.join(sorted(g['values']))}" for g in filter_groups]
    cache_key = f"filter:{':'.join(cache_parts)}" if cache_parts else "filter:all"

    if cache_key in _cache:
        return _cache[cache_key]

    # Get all specs with implementations
    repo = SpecRepository(db)
    all_specs = await repo.get_all()

    # Build lookup of spec_id -> (spec_obj, tags)
    spec_lookup: dict = {}
    for spec_obj in all_specs:
        if spec_obj.impls:
            spec_lookup[spec_obj.id] = {
                "spec": spec_obj,
                "tags": spec_obj.tags or {},
            }

    # Helper function to check if an image matches a set of filter groups
    def image_matches_groups(spec_id: str, library: str, groups: list[dict]) -> bool:
        if spec_id not in spec_lookup:
            return False
        spec_tags = spec_lookup[spec_id]["tags"]

        for group in groups:
            category = group["category"]
            values = group["values"]

            if category == "lib":
                if library not in values:
                    return False
            elif category == "spec":
                if spec_id not in values:
                    return False
            elif category == "plot":
                spec_plot_types = spec_tags.get("plot_type", [])
                if not any(v in spec_plot_types for v in values):
                    return False
            elif category == "data":
                spec_data_types = spec_tags.get("data_type", [])
                if not any(v in spec_data_types for v in values):
                    return False
            elif category == "dom":
                spec_domains = spec_tags.get("domain", [])
                if not any(v in spec_domains for v in values):
                    return False
            elif category == "feat":
                spec_features = spec_tags.get("features", [])
                if not any(v in spec_features for v in values):
                    return False
        return True

    # Build list of all images with metadata
    all_images: list[dict] = []
    for spec_obj in all_specs:
        if not spec_obj.impls:
            continue
        for impl in spec_obj.impls:
            if impl.preview_url:
                all_images.append({
                    "spec_id": spec_obj.id,
                    "library": impl.library_id,
                    "url": impl.preview_url,
                    "thumb": impl.preview_thumb,
                    "html": impl.preview_html,
                    "code": impl.code,
                })

    # Filter images based on all groups
    filtered_images = [
        img for img in all_images
        if image_matches_groups(img["spec_id"], img["library"], filter_groups)
    ]

    # Build a lookup of spec_id -> tags for all specs
    spec_id_to_tags: dict = {}
    for spec_obj in all_specs:
        if spec_obj.impls:
            spec_id_to_tags[spec_obj.id] = spec_obj.tags or {}

    # Calculate GLOBAL counts (for OR additions - expands results)
    # This shows total available regardless of current filters
    global_counts: dict = {
        "lib": {},
        "spec": {},
        "plot": {},
        "data": {},
        "dom": {},
        "feat": {},
    }

    for spec_obj in all_specs:
        if not spec_obj.impls:
            continue
        spec_tags = spec_obj.tags or {}

        for impl in spec_obj.impls:
            if not impl.preview_url:
                continue

            # Count library
            global_counts["lib"][impl.library_id] = global_counts["lib"].get(impl.library_id, 0) + 1

            # Count spec ID
            global_counts["spec"][spec_obj.id] = global_counts["spec"].get(spec_obj.id, 0) + 1

            # Count tags
            for plot_type in spec_tags.get("plot_type", []):
                global_counts["plot"][plot_type] = global_counts["plot"].get(plot_type, 0) + 1

            for data_type in spec_tags.get("data_type", []):
                global_counts["data"][data_type] = global_counts["data"].get(data_type, 0) + 1

            for domain in spec_tags.get("domain", []):
                global_counts["dom"][domain] = global_counts["dom"].get(domain, 0) + 1

            for feature in spec_tags.get("features", []):
                global_counts["feat"][feature] = global_counts["feat"].get(feature, 0) + 1

    # Sort global counts
    for category in global_counts:
        global_counts[category] = dict(sorted(global_counts[category].items(), key=lambda x: (-x[1], x[0])))

    # Calculate CONTEXTUAL counts (for AND additions - narrows results)
    # This shows how many results each additional filter would give
    counts: dict = {
        "lib": {},
        "spec": {},
        "plot": {},
        "data": {},
        "dom": {},
        "feat": {},
    }

    # Count from filtered images
    for img in filtered_images:
        spec_id = img["spec_id"]
        library = img["library"]
        spec_tags = spec_id_to_tags.get(spec_id, {})

        # Count library
        counts["lib"][library] = counts["lib"].get(library, 0) + 1

        # Count spec ID
        counts["spec"][spec_id] = counts["spec"].get(spec_id, 0) + 1

        # Count tags
        for plot_type in spec_tags.get("plot_type", []):
            counts["plot"][plot_type] = counts["plot"].get(plot_type, 0) + 1

        for data_type in spec_tags.get("data_type", []):
            counts["data"][data_type] = counts["data"].get(data_type, 0) + 1

        for domain in spec_tags.get("domain", []):
            counts["dom"][domain] = counts["dom"].get(domain, 0) + 1

        for feature in spec_tags.get("features", []):
            counts["feat"][feature] = counts["feat"].get(feature, 0) + 1

    # Sort contextual counts
    for category in counts:
        counts[category] = dict(sorted(counts[category].items(), key=lambda x: (-x[1], x[0])))

    # Calculate OR preview counts for each filter group
    # For each group, apply all OTHER groups' filters and count each value
    # This shows what would be added if we add a value with OR to that group
    or_counts: list[dict] = []

    for group_idx, group in enumerate(filter_groups):
        # Get all other groups (excluding this one)
        other_groups = [g for i, g in enumerate(filter_groups) if i != group_idx]

        # Filter images with only the other groups' filters
        images_with_other_filters = [
            img for img in all_images
            if image_matches_groups(img["spec_id"], img["library"], other_groups)
        ]

        # Count each value for this group's category
        category = group["category"]
        group_counts: dict[str, int] = {}

        for img in images_with_other_filters:
            spec_id = img["spec_id"]
            library = img["library"]
            spec_tags = spec_id_to_tags.get(spec_id, {})

            if category == "lib":
                group_counts[library] = group_counts.get(library, 0) + 1
            elif category == "spec":
                group_counts[spec_id] = group_counts.get(spec_id, 0) + 1
            elif category == "plot":
                for v in spec_tags.get("plot_type", []):
                    group_counts[v] = group_counts.get(v, 0) + 1
            elif category == "data":
                for v in spec_tags.get("data_type", []):
                    group_counts[v] = group_counts.get(v, 0) + 1
            elif category == "dom":
                for v in spec_tags.get("domain", []):
                    group_counts[v] = group_counts.get(v, 0) + 1
            elif category == "feat":
                for v in spec_tags.get("features", []):
                    group_counts[v] = group_counts.get(v, 0) + 1

        # Sort by count descending
        group_counts = dict(sorted(group_counts.items(), key=lambda x: (-x[1], x[0])))
        or_counts.append(group_counts)

    result = FilteredPlotsResponse(
        total=len(filtered_images),
        images=filtered_images,
        counts=counts,
        globalCounts=global_counts,
        orCounts=or_counts,
    )
    _cache[cache_key] = result
    return result


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
            raise HTTPException(status_code=502, detail=f"Failed to fetch image: {e}") from e

    # Return as downloadable file
    filename = f"{spec_id}-{library}.png"
    return Response(
        content=response.content,
        media_type="image/png",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ============================================================================
# SEO Endpoints
# ============================================================================


@app.get("/sitemap.xml")
async def get_sitemap(db: AsyncSession = Depends(get_db)):
    """
    Generate dynamic XML sitemap for SEO.

    Includes all specs with implementations and all libraries.
    """
    cache_key = "sitemap_xml"
    if cache_key in _cache:
        return Response(content=_cache[cache_key], media_type="application/xml")

    # Build XML lines
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "  <url><loc>https://pyplots.ai/</loc></url>",
    ]

    # Add spec URLs (only specs with implementations)
    if is_db_configured():
        repo = SpecRepository(db)
        specs = await repo.get_all()
        for spec in specs:
            if spec.impls:  # Only include specs with implementations
                spec_id = html.escape(spec.id)
                xml_lines.append(f"  <url><loc>https://pyplots.ai/?spec={spec_id}</loc></url>")

    # Add library URLs (static list)
    for lib in LIBRARIES_SEED:
        lib_id = html.escape(lib["id"])
        xml_lines.append(f"  <url><loc>https://pyplots.ai/?lib={lib_id}</loc></url>")

    xml_lines.append("</urlset>")
    xml = "\n".join(xml_lines)

    _cache[cache_key] = xml
    return Response(content=xml, media_type="application/xml")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
