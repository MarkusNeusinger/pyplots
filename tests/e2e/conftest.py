"""
E2E test fixtures with real PostgreSQL database.

Uses a separate 'test_e2e' schema to isolate test data from production.
Tests are skipped if DATABASE_URL is not set or database is unreachable.

Connection modes:
- Local: Direct DATABASE_URL from .env
- CI: DATABASE_URL via Cloud SQL Proxy (localhost:5432 -> Cloud SQL)

Note: These tests must NOT be run with pytest-xdist parallelization
as multiple workers would conflict on the shared test_e2e schema.
"""

import asyncio
import os

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.database.models import Base


TEST_SCHEMA = "test_e2e"
CONNECTION_TIMEOUT = 10  # seconds - skip tests if DB unreachable

# Test data constants
TEST_IMAGE_URL = "https://storage.googleapis.com/pyplots-images/test/plot.png"
TEST_THUMB_URL = "https://storage.googleapis.com/pyplots-images/test/thumb.png"


def _get_database_url():
    """Get DATABASE_URL from environment, loading .env if needed."""
    from dotenv import load_dotenv

    load_dotenv()

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        return None

    # Ensure async driver
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
    elif database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+asyncpg://")

    return database_url


@pytest_asyncio.fixture(scope="function")
async def pg_engine():
    """
    Create PostgreSQL engine and setup test schema.

    Creates a separate 'test_e2e' schema to isolate tests from production data.
    The schema is dropped and recreated for each test.
    Skips tests if database is unreachable.
    """
    database_url = _get_database_url()
    if not database_url:
        pytest.skip("DATABASE_URL not set - skipping PostgreSQL E2E tests")

    # Create temporary engine for schema setup
    temp_engine = create_async_engine(database_url, echo=False, connect_args={"timeout": CONNECTION_TIMEOUT})
    try:
        async with asyncio.timeout(CONNECTION_TIMEOUT + 2):
            async with temp_engine.begin() as conn:
                await conn.execute(text(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE"))
                await conn.execute(text(f"CREATE SCHEMA {TEST_SCHEMA}"))
        await temp_engine.dispose()
    except (TimeoutError, asyncio.TimeoutError, OSError) as e:
        await temp_engine.dispose()
        pytest.skip(f"Database unreachable (timeout) - skipping E2E tests: {e}")
    except Exception as e:
        await temp_engine.dispose()
        pytest.skip(f"Database connection failed - skipping E2E tests: {e}")

    # Create main engine with search_path set at connection level
    engine = create_async_engine(
        database_url,
        echo=False,
        connect_args={"server_settings": {"search_path": TEST_SCHEMA}, "timeout": CONNECTION_TIMEOUT},
    )

    # Create tables in test schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup: Drop entire test schema
    async with engine.begin() as conn:
        await conn.execute(text(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE"))
    await engine.dispose()


@pytest_asyncio.fixture
async def pg_session(pg_engine):
    """Create session with test schema (search_path set at engine level)."""
    async_session = async_sessionmaker(pg_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
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
