"""
FastAPI dependencies for pyplots API.

Reusable dependencies for database access, authentication, etc.
"""

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db, is_db_configured


async def require_db(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    """
    Dependency that ensures database is configured and returns session.

    Raises:
        HTTPException: 503 if database is not configured.

    Returns:
        AsyncSession: Database session.
    """
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    return db


def db_or_fallback(fallback_value):
    """
    Create a dependency that returns fallback value if DB not configured.

    Args:
        fallback_value: Value to return when database is not available.

    Returns:
        Dependency function.
    """

    async def dependency(db: AsyncSession = Depends(get_db)):
        if not is_db_configured():
            return None, fallback_value
        return db, None

    return dependency
