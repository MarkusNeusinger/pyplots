"""
SQLAlchemy ORM models for pyplots.

Defines database tables for specs, libraries, and impls.
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.database.connection import Base


class Spec(Base):
    """Plot specification - library-agnostic definition of a plot type."""

    __tablename__ = "specs"

    # Identification
    id: Mapped[str] = mapped_column(String, primary_key=True)  # e.g., "scatter-basic"
    title: Mapped[str] = mapped_column(String, nullable=False)

    # From spec.md
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Prose text
    applications: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)  # Use cases
    data: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)  # Data requirements
    notes: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)  # Optional hints

    # From metadata.yaml
    created: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # When spec was created
    issue: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # GitHub issue number
    suggested: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # GitHub username
    tags: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True
    )  # {plot_type, domain, features, audience, data_type}
    history: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)  # Spec update history

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

    # Relationships
    impls: Mapped[list["Impl"]] = relationship("Impl", back_populates="library", cascade="all, delete-orphan")


class Impl(Base):
    """Library-specific implementation of a spec."""

    __tablename__ = "impls"

    # Identification
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
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
    tested: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    # Quality & Generation
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    generated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    generated_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Model ID
    issue: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # GitHub Issue
    workflow_run: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)  # GitHub Actions run ID

    # Quality evaluation details
    evaluator_scores: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)  # Per-LLM scores
    quality_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Evaluation feedback
    improvements_suggested: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)  # Suggested fixes

    # Version history
    history: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)  # Previous versions

    # System
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    spec: Mapped["Spec"] = relationship("Spec", back_populates="impls")
    library: Mapped["Library"] = relationship("Library", back_populates="impls")

    # Unique constraint
    __table_args__ = (UniqueConstraint("spec_id", "library_id", name="uq_impl"),)


# Seed data for libraries
LIBRARIES_SEED = [
    {"id": "matplotlib", "name": "Matplotlib", "version": "3.9.0", "documentation_url": "https://matplotlib.org"},
    {"id": "seaborn", "name": "Seaborn", "version": "0.13.0", "documentation_url": "https://seaborn.pydata.org"},
    {"id": "plotly", "name": "Plotly", "version": "5.18.0", "documentation_url": "https://plotly.com/python"},
    {"id": "bokeh", "name": "Bokeh", "version": "3.4.0", "documentation_url": "https://bokeh.org"},
    {"id": "altair", "name": "Altair", "version": "5.2.0", "documentation_url": "https://altair-viz.github.io"},
    {"id": "plotnine", "name": "plotnine", "version": "0.13.0", "documentation_url": "https://plotnine.readthedocs.io"},
    {"id": "pygal", "name": "Pygal", "version": "3.0.0", "documentation_url": "http://www.pygal.org"},
    {"id": "highcharts", "name": "Highcharts", "version": "1.10.0", "documentation_url": "https://www.highcharts.com"},
    {"id": "letsplot", "name": "lets-plot", "version": "4.5.0", "documentation_url": "https://lets-plot.org"},
]
