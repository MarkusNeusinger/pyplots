"""
Async SQLAlchemy database connection for pyplots.

Supports two connection modes:
1. Cloud SQL Connector (recommended for Cloud Run) - uses INSTANCE_CONNECTION_NAME
2. Direct connection via DATABASE_URL (for local development)
"""

import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool


logger = logging.getLogger(__name__)

# Environment variables
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME", "")
DATABASE_URL = os.getenv("DATABASE_URL", "")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "pyplots")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Global instances
engine = None
AsyncSessionLocal: Optional[async_sessionmaker] = None
_connector = None


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


async def _create_cloud_sql_engine():
    """Create engine using Cloud SQL Python Connector."""
    global _connector

    from google.cloud.sql.connector import Connector, IPTypes

    # Create connector instance
    _connector = Connector()

    # Use PUBLIC IP (no VPC needed, free)
    ip_type = IPTypes.PUBLIC

    # Check if running on Cloud Run (automatic auth)
    is_cloud_run = os.getenv("K_SERVICE") is not None
    if is_cloud_run:
        logger.info("Running on Cloud Run - using automatic IAM authentication")

    async def get_conn():
        conn = await _connector.connect_async(
            INSTANCE_CONNECTION_NAME, "asyncpg", user=DB_USER, password=DB_PASS, db=DB_NAME, ip_type=ip_type
        )
        return conn

    engine = create_async_engine(
        "postgresql+asyncpg://",
        async_creator=get_conn,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        echo=ENVIRONMENT == "development",
    )

    logger.info(f"Created Cloud SQL engine: {INSTANCE_CONNECTION_NAME} (PUBLIC IP)")
    return engine


def _create_direct_engine():
    """Create engine using direct DATABASE_URL connection."""
    url = DATABASE_URL

    # Ensure async driver
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://")
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://")

    # Use NullPool for testing to avoid connection issues
    poolclass = NullPool if ENVIRONMENT == "test" else None

    engine = create_async_engine(
        url,
        poolclass=poolclass,
        pool_size=5 if not poolclass else None,
        max_overflow=10 if not poolclass else None,
        pool_pre_ping=True if not poolclass else False,
        echo=ENVIRONMENT == "development",
    )

    # Log without exposing password
    safe_url = url.split("@")[-1] if "@" in url else "local"
    logger.info(f"Created direct database engine: {safe_url}")
    return engine


async def init_db() -> None:
    """
    Initialize database connection.

    Priority:
    1. DATABASE_URL (direct connection) - for local development
    2. Cloud SQL Connector (INSTANCE_CONNECTION_NAME) - for Cloud Run
    """
    global engine, AsyncSessionLocal

    if engine is not None:
        return  # Already initialized

    # Prefer direct connection for local development
    if DATABASE_URL:
        engine = _create_direct_engine()
    elif INSTANCE_CONNECTION_NAME:
        # Cloud SQL Connector - requires ADC or runs on Cloud Run
        try:
            engine = await _create_cloud_sql_engine()
        except Exception as e:
            logger.error(f"Cloud SQL Connector failed: {e}")
            logger.error("Set DATABASE_URL for local development or configure ADC")
            raise
    else:
        logger.warning("No database configuration found - running without database")
        return

    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def close_db() -> None:
    """Close database connections and cleanup."""
    global engine, AsyncSessionLocal, _connector

    if engine:
        await engine.dispose()
        engine = None
        AsyncSessionLocal = None
        logger.info("Database engine disposed")

    if _connector:
        await _connector.close_async()
        _connector = None
        logger.info("Cloud SQL connector closed")


async def get_db() -> AsyncGenerator[AsyncSession | None, None]:
    """
    Dependency that provides a database session.

    Yields:
        AsyncSession if database is configured, None otherwise
    """
    # Lazy initialization
    if engine is None:
        await init_db()

    if AsyncSessionLocal is None:
        yield None
        return

    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database session (for scripts).

    Usage:
        async with get_db_context() as session:
            # Use session here
    """
    if engine is None:
        await init_db()

    if AsyncSessionLocal is None:
        raise RuntimeError("Database not configured")

    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def is_db_configured() -> bool:
    """Check if database is configured (credentials available)."""
    return bool(INSTANCE_CONNECTION_NAME or DATABASE_URL)
