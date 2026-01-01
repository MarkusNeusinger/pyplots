"""
SQLAlchemy ORM models for pyplots.

Defines database tables for specs, libraries, and impls.
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.constants import LIBRARIES_METADATA
from core.database.connection import Base
from core.database.types import StringArray, UniversalJSON, UniversalUUID


class Spec(Base):
    """Plot specification - library-agnostic definition of a plot type."""

    __tablename__ = "specs"

    # Identification
    id: Mapped[str] = mapped_column(String, primary_key=True)  # e.g., "scatter-basic"
    title: Mapped[str] = mapped_column(String, nullable=False)

    # From spec.md
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Prose text
    applications: Mapped[list[str]] = mapped_column(StringArray, default=list)  # Use cases
    data: Mapped[list[str]] = mapped_column(StringArray, default=list)  # Data requirements
    notes: Mapped[list[str]] = mapped_column(StringArray, default=list)  # Optional hints

    # From metadata.yaml
    created: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # When spec was first created
    updated: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # When spec was last modified
    issue: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # GitHub issue number
    suggested: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # GitHub username
    tags: Mapped[Optional[dict]] = mapped_column(
        UniversalJSON, nullable=True
    )  # {plot_type, data_type, domain, features}

    # System
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    impls: Mapped[list["Impl"]] = relationship("Impl", back_populates="spec", cascade="all, delete-orphan")


class Library(Base):
    """Supported plotting library."""

    __tablename__ = "libraries"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # e.g., "matplotlib"
    name: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Matplotlib"
    version: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Current version
    documentation_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Short description

    # Relationships
    impls: Mapped[list["Impl"]] = relationship("Impl", back_populates="library", cascade="all, delete-orphan")


class Impl(Base):
    """Library-specific implementation of a spec."""

    __tablename__ = "impls"

    # Identification
    id: Mapped[str] = mapped_column(UniversalUUID, primary_key=True, default=lambda: str(uuid4()))
    spec_id: Mapped[str] = mapped_column(String, ForeignKey("specs.id", ondelete="CASCADE"), nullable=False)
    library_id: Mapped[str] = mapped_column(String, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False)

    # Code
    code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Python source

    # Previews (filled by workflow, synced from metadata YAML)
    preview_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Full PNG
    preview_thumb: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Thumbnail PNG
    preview_html: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Interactive HTML

    # Creation versions (filled by workflow)
    python_version: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # e.g., "3.13"
    library_version: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # e.g., "3.9.0"

    # Test matrix: [{"py": "3.11", "lib": "3.8.5", "ok": true}, ...]
    tested: Mapped[Optional[list]] = mapped_column(UniversalJSON, nullable=True)

    # Quality & Generation
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    generated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # First generation
    updated: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Last update
    generated_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Model ID
    issue: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # GitHub Issue
    workflow_run: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)  # GitHub Actions run ID

    # Review feedback (structured arrays from impl-review)
    review_strengths: Mapped[list[str]] = mapped_column(StringArray, default=list)  # What's good
    review_weaknesses: Mapped[list[str]] = mapped_column(StringArray, default=list)  # What needs work

    # Extended review data (from issue #2845)
    review_image_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # AI's visual description
    review_criteria_checklist: Mapped[Optional[dict]] = mapped_column(UniversalJSON, nullable=True)  # Detailed scoring
    review_verdict: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # "APPROVED" or "REJECTED"

    # System
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    spec: Mapped["Spec"] = relationship("Spec", back_populates="impls")
    library: Mapped["Library"] = relationship("Library", back_populates="impls")

    # Unique constraint
    __table_args__ = (UniqueConstraint("spec_id", "library_id", name="uq_impl"),)


# Seed data for libraries (re-exported from core.constants)
LIBRARIES_SEED = LIBRARIES_METADATA
