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
    created: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # When spec was first created
    updated: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # When spec was last modified
    issue: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # GitHub issue number
    suggested: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # GitHub username
    tags: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)  # {plot_type, data_type, domain, features}

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
    generated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # First generation
    updated: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Last update
    generated_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Model ID
    issue: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # GitHub Issue
    workflow_run: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)  # GitHub Actions run ID

    # Review feedback (structured arrays from impl-review)
    review_strengths: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)  # What's good
    review_weaknesses: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)  # What needs work

    # System
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    spec: Mapped["Spec"] = relationship("Spec", back_populates="impls")
    library: Mapped["Library"] = relationship("Library", back_populates="impls")

    # Unique constraint
    __table_args__ = (UniqueConstraint("spec_id", "library_id", name="uq_impl"),)


# Seed data for libraries (descriptions from official websites)
LIBRARIES_SEED = [
    {
        "id": "altair",
        "name": "Altair",
        "version": "5.2.0",
        "documentation_url": "https://altair-viz.github.io",
        "description": "Declarative visualization library for Python. Its simple, friendly and consistent API, built on top of the powerful Vega-Lite grammar, empowers you to spend less time writing code and more time exploring your data.",
    },
    {
        "id": "bokeh",
        "name": "Bokeh",
        "version": "3.4.0",
        "documentation_url": "https://bokeh.org",
        "description": "Interactive visualization library that makes it simple to create common plots, while also handling custom or specialized use-cases. Work in Python close to all the PyData tools you're already familiar with.",
    },
    {
        "id": "highcharts",
        "name": "Highcharts",
        "version": "1.10.0",
        "documentation_url": "https://www.highcharts.com",
        "description": "Powerful data visualization for real-world apps. Fast to implement, endlessly flexible. Makes it easy for developers to create charts and dashboards for web and mobile platforms.",
    },
    {
        "id": "letsplot",
        "name": "lets-plot",
        "version": "4.5.0",
        "documentation_url": "https://lets-plot.org",
        "description": "Multiplatform plotting library built on the principles of the Grammar of Graphics. A faithful adaptation of R's ggplot2 that extends Grammar of Graphics principles to both Python and Kotlin.",
    },
    {
        "id": "matplotlib",
        "name": "Matplotlib",
        "version": "3.9.0",
        "documentation_url": "https://matplotlib.org",
        "description": "Comprehensive library for creating static, animated, and interactive visualizations in Python. Matplotlib makes easy things easy and hard things possible.",
    },
    {
        "id": "plotly",
        "name": "Plotly",
        "version": "5.18.0",
        "documentation_url": "https://plotly.com/python",
        "description": "Python graphing library that makes interactive, publication-quality graphs. Create line plots, scatter plots, area charts, bar charts, error bars, box plots, histograms, heatmaps, subplots, and more.",
    },
    {
        "id": "plotnine",
        "name": "plotnine",
        "version": "0.13.0",
        "documentation_url": "https://plotnine.org",
        "description": "A grammar of graphics for Python. Data visualization package based on the grammar of graphics, a coherent system for describing and building graphs. From ad-hoc plots to publication-ready figures.",
    },
    {
        "id": "pygal",
        "name": "Pygal",
        "version": "3.0.0",
        "documentation_url": "http://www.pygal.org",
        "description": "Beautiful python charting. Simple python charting library that creates SVG charts that are both beautiful and easy to customize.",
    },
    {
        "id": "seaborn",
        "name": "Seaborn",
        "version": "0.13.0",
        "documentation_url": "https://seaborn.pydata.org",
        "description": "Python data visualization library based on matplotlib. Provides a high-level interface for drawing attractive and informative statistical graphics.",
    },
]
