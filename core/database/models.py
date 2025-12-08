"""
SQLAlchemy ORM models for pyplots.

Defines database tables for specs, libraries, and implementations.
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.database.connection import Base


class Spec(Base):
    """Plot specification - library-agnostic definition of a plot type."""

    __tablename__ = "specs"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # e.g., "scatter-basic"
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_requirements: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)
    optional_params: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    # Structured tags from metadata/*.yaml (plot_type, domain, features, audience, data_type)
    structured_tags: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    implementations: Mapped[list["Implementation"]] = relationship(
        "Implementation", back_populates="spec", cascade="all, delete-orphan"
    )


class Library(Base):
    """Supported plotting library."""

    __tablename__ = "libraries"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # e.g., "matplotlib"
    name: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Matplotlib"
    version: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    documentation_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    implementations: Mapped[list["Implementation"]] = relationship(
        "Implementation", back_populates="library", cascade="all, delete-orphan"
    )


class Implementation(Base):
    """Library-specific implementation of a spec."""

    __tablename__ = "implementations"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    spec_id: Mapped[str] = mapped_column(String, ForeignKey("specs.id", ondelete="CASCADE"), nullable=False)
    library_id: Mapped[str] = mapped_column(String, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False)
    plot_function: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "scatter", "bar"
    variant: Mapped[str] = mapped_column(String, nullable=False, default="default")
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    preview_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # GCS URL
    python_version: Mapped[str] = mapped_column(String, default="3.12+")
    tested: Mapped[bool] = mapped_column(Boolean, default=False)
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Generation metadata (from metadata/*.yaml)
    generated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    generated_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Model ID, e.g., "claude-opus-4-5-20251101"
    workflow_run: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # GitHub Actions workflow run ID
    issue_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # GitHub Issue number

    # Quality evaluation details
    evaluator_scores: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)  # [{"model": "...", "score": 92}, ...]
    quality_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    improvements_suggested: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)  # ["suggestion1", "suggestion2"]

    # Relationships
    spec: Mapped["Spec"] = relationship("Spec", back_populates="implementations")
    library: Mapped["Library"] = relationship("Library", back_populates="implementations")

    # Unique constraint
    __table_args__ = (UniqueConstraint("spec_id", "library_id", "variant", name="uq_implementation"),)


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
