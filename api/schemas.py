"""
Pydantic schemas for pyplots API.

Centralized schema definitions for request/response models.
"""

from typing import Optional

from pydantic import BaseModel


class ImplementationResponse(BaseModel):
    """Implementation details for a single library."""

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
    # Review fields
    review_strengths: list[str] = []
    review_weaknesses: list[str] = []
    review_image_description: Optional[str] = None
    review_criteria_checklist: Optional[dict] = None
    review_verdict: Optional[str] = None


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
    created: Optional[str] = None
    updated: Optional[str] = None
    implementations: list[ImplementationResponse] = []


class SpecListItem(BaseModel):
    """Spec list item with summary info."""

    id: str
    title: str
    description: Optional[str] = None
    tags: Optional[dict] = None
    library_count: int = 0


class ImageResponse(BaseModel):
    """Image/plot response for grid display."""

    spec_id: str
    library: str
    url: Optional[str] = None
    thumb: Optional[str] = None
    html: Optional[str] = None
    code: Optional[str] = None


class FilterCountsResponse(BaseModel):
    """Counts for filter categories."""

    lib: dict[str, int] = {}
    spec: dict[str, int] = {}
    plot: dict[str, int] = {}
    data: dict[str, int] = {}
    dom: dict[str, int] = {}
    feat: dict[str, int] = {}


class FilteredPlotsResponse(BaseModel):
    """Response for filtered plots endpoint."""

    total: int
    images: list[dict]  # Using dict for flexibility, could be list[ImageResponse]
    counts: dict
    globalCounts: dict
    orCounts: list[dict]


class LibraryInfo(BaseModel):
    """Library information."""

    id: str
    name: str
    version: Optional[str] = None
    documentation_url: Optional[str] = None
    description: Optional[str] = None


class StatsResponse(BaseModel):
    """Platform statistics."""

    specs: int
    plots: int
    libraries: int
