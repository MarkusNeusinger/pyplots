"""
Async SQLAlchemy database connection for pyplots.

Provides database engine, session factory, and dependency injection for FastAPI.
"""

import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Create async engine (only if DATABASE_URL is set)
engine = None
AsyncSessionLocal = None

if DATABASE_URL:
    engine = create_async_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        echo=False,
    )
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


async def get_db() -> AsyncGenerator[AsyncSession | None, None]:
    """
    Dependency that provides a database session.

    Yields:
        AsyncSession if database is configured, None otherwise
    """
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


def is_db_configured() -> bool:
    """Check if database is configured and available."""
    return engine is not None and AsyncSessionLocal is not None
