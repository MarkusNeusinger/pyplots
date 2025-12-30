"""
E2E test fixtures with real PostgreSQL database.

Uses a separate 'test_e2e' schema to isolate test data from production.
Supports two connection modes:
1. Cloud SQL Connector (CI) - uses INSTANCE_CONNECTION_NAME
2. Direct connection (local) - uses DATABASE_URL

Tests are skipped if neither is configured or database is unreachable.

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

# Store Cloud SQL connectors for cleanup (can't attach to engine objects)
_connectors = []


def _get_connection_config():
    """Get database connection config.

    Prefers DATABASE_URL for local development (simpler, no event loop issues).
    Falls back to Cloud SQL Connector for CI environments.
    """
    from dotenv import load_dotenv

    load_dotenv()

    # Prefer DATABASE_URL for local development
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        # Ensure async driver
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
        elif database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+asyncpg://")
        return {"mode": "direct", "url": database_url}

    # Fall back to Cloud SQL Connector (for CI)
    instance_conn = os.environ.get("INSTANCE_CONNECTION_NAME")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")

    if instance_conn and db_user and db_pass and db_name:
        return {
            "mode": "cloud_sql",
            "instance": instance_conn,
            "user": db_user,
            "password": db_pass,
            "database": db_name,
        }

    return None


async def _create_cloud_sql_engine(config, search_path=None):
    """Create async engine using Cloud SQL Connector with asyncpg."""
    from google.cloud.sql.connector import Connector, IPTypes

    connector = Connector()
    _connectors.append(connector)  # Store for cleanup

    async def getconn():
        conn = await connector.connect_async(
            config["instance"],
            "asyncpg",
            user=config["user"],
            password=config["password"],
            db=config["database"],
            ip_type=IPTypes.PUBLIC,
        )
        if search_path:
            await conn.execute(f"SET search_path TO {search_path}")
        return conn

    return create_async_engine("postgresql+asyncpg://", async_creator=getconn, echo=False)


async def _create_direct_engine(url, search_path=None):
    """Create async engine using direct DATABASE_URL connection."""
    connect_args = {"timeout": CONNECTION_TIMEOUT}
    if search_path:
        connect_args["server_settings"] = {"search_path": search_path}

    return create_async_engine(url, echo=False, connect_args=connect_args)


async def _cleanup_connectors():
    """Clean up all Cloud SQL connectors."""
    global _connectors
    for connector in _connectors:
        await connector.close_async()
    _connectors = []


@pytest_asyncio.fixture(scope="function")
async def pg_engine():
    """
    Create PostgreSQL engine and setup test schema.

    Creates a separate 'test_e2e' schema to isolate tests from production data.
    The schema is dropped and recreated for each test.
    Skips tests if database is unreachable.
    """
    config = _get_connection_config()
    if not config:
        pytest.skip("No database configured - skipping PostgreSQL E2E tests")

    # Create temporary engine for schema setup
    try:
        if config["mode"] == "cloud_sql":
            temp_engine = await _create_cloud_sql_engine(config)
        else:
            temp_engine = await _create_direct_engine(config["url"])

        async with asyncio.timeout(CONNECTION_TIMEOUT + 2):
            async with temp_engine.begin() as conn:
                await conn.execute(text(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE"))
                await conn.execute(text(f"CREATE SCHEMA {TEST_SCHEMA}"))

        await temp_engine.dispose()

    except (TimeoutError, asyncio.TimeoutError, OSError) as e:
        await _cleanup_connectors()
        pytest.skip(f"Database unreachable (timeout) - skipping E2E tests: {e}")
    except Exception as e:
        await _cleanup_connectors()
        pytest.skip(f"Database connection failed - skipping E2E tests: {e}")

    # Create main engine with search_path set
    if config["mode"] == "cloud_sql":
        engine = await _create_cloud_sql_engine(config, search_path=TEST_SCHEMA)
    else:
        engine = await _create_direct_engine(config["url"], search_path=TEST_SCHEMA)

    # Create tables in test schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup: Drop entire test schema
    async with engine.begin() as conn:
        await conn.execute(text(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE"))

    await engine.dispose()
    await _cleanup_connectors()


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
