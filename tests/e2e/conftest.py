"""
E2E test fixtures with real PostgreSQL database.

Uses a separate 'test_e2e' schema to isolate test data from production.
Tests are skipped if DATABASE_URL is not set.
"""

import os

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.database.models import Base


TEST_SCHEMA = "test_e2e"

# Test data constants
TEST_IMAGE_URL = "https://storage.googleapis.com/pyplots-images/test/plot.png"
TEST_THUMB_URL = "https://storage.googleapis.com/pyplots-images/test/thumb.png"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for session-scoped async fixtures."""
    import asyncio

    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def pg_engine():
    """
    Create PostgreSQL engine and setup test schema.

    Creates a separate 'test_e2e' schema to isolate tests from production data.
    The schema is dropped and recreated at the start of the test session.
    """
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL not set - skipping PostgreSQL E2E tests")

    engine = create_async_engine(database_url, echo=False)

    # Create test schema and tables
    async with engine.begin() as conn:
        await conn.execute(text(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE"))
        await conn.execute(text(f"CREATE SCHEMA {TEST_SCHEMA}"))
        await conn.execute(text(f"SET search_path TO {TEST_SCHEMA}"))
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup: Drop entire test schema
    async with engine.begin() as conn:
        await conn.execute(text(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE"))
    await engine.dispose()


@pytest.fixture
async def pg_session(pg_engine):
    """Create session with test schema."""
    async_session = async_sessionmaker(pg_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        # Ensure we're in test schema
        await session.execute(text(f"SET search_path TO {TEST_SCHEMA}"))
        yield session
        await session.rollback()


@pytest.fixture
async def pg_db_with_data(pg_session):
    """
    Seed test schema with sample data.

    Creates the same test data as tests/conftest.py:test_db_with_data
    but in the PostgreSQL test schema.
    """
    from core.database.models import Impl, Library, Spec

    # Create libraries
    matplotlib_lib = Library(
        id="matplotlib",
        name="Matplotlib",
        version="3.10.0",
        documentation_url="https://matplotlib.org",
        description="Comprehensive library for visualizations",
    )
    seaborn_lib = Library(
        id="seaborn",
        name="Seaborn",
        version="0.13.0",
        documentation_url="https://seaborn.pydata.org",
        description="Statistical data visualization",
    )
    pg_session.add_all([matplotlib_lib, seaborn_lib])

    # Create specs
    scatter_spec = Spec(
        id="scatter-basic",
        title="Basic Scatter Plot",
        description="A basic scatter plot",
        applications=["data visualization", "correlation analysis"],
        data=["numeric"],
        notes=["Use for 2D data"],
        tags={"plot_type": ["scatter"], "domain": ["statistics"], "data_type": ["numeric"], "features": ["basic"]},
        issue=42,
        suggested="contributor",
    )
    bar_spec = Spec(
        id="bar-grouped",
        title="Grouped Bar Chart",
        description="A grouped bar chart",
        applications=["comparisons"],
        data=["categorical", "numeric"],
        notes=["Good for comparing categories"],
        tags={"plot_type": ["bar"], "domain": ["statistics"], "data_type": ["categorical"], "features": ["grouped"]},
        issue=43,
        suggested="contributor2",
    )
    pg_session.add_all([scatter_spec, bar_spec])
    await pg_session.commit()

    # Create implementations
    scatter_matplotlib = Impl(
        spec_id="scatter-basic",
        library_id="matplotlib",
        code="import matplotlib.pyplot as plt\n# scatter plot code",
        preview_url=TEST_IMAGE_URL.replace("plot", "scatter-matplotlib"),
        preview_thumb=TEST_THUMB_URL.replace("thumb", "scatter-matplotlib-thumb"),
        quality_score=92.5,
        generated_by="claude",
        python_version="3.13",
        library_version="3.10.0",
    )
    scatter_seaborn = Impl(
        spec_id="scatter-basic",
        library_id="seaborn",
        code="import seaborn as sns\n# scatter plot code",
        preview_url=TEST_IMAGE_URL.replace("plot", "scatter-seaborn"),
        preview_thumb=TEST_THUMB_URL.replace("thumb", "scatter-seaborn-thumb"),
        quality_score=95.0,
        generated_by="claude",
        python_version="3.13",
        library_version="0.13.0",
    )
    bar_matplotlib = Impl(
        spec_id="bar-grouped",
        library_id="matplotlib",
        code="import matplotlib.pyplot as plt\n# bar chart code",
        preview_url=TEST_IMAGE_URL.replace("plot", "bar-matplotlib"),
        quality_score=88.0,
        generated_by="claude",
        python_version="3.13",
        library_version="3.10.0",
    )
    pg_session.add_all([scatter_matplotlib, scatter_seaborn, bar_matplotlib])
    await pg_session.commit()

    # Expire all cached objects to ensure fresh loading with relationships
    pg_session.expire_all()

    yield pg_session
