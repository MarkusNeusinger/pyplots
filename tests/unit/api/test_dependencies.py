"""
Tests for api/dependencies.py.

Tests the reusable FastAPI dependencies for database access.
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from api.dependencies import optional_db, require_db


class TestRequireDb:
    """Tests for require_db dependency."""

    @pytest.mark.asyncio
    async def test_returns_db_when_configured(self) -> None:
        """Should return db session when database is configured."""
        mock_db = AsyncMock()

        with patch("api.dependencies.is_db_configured", return_value=True):
            result = await require_db(db=mock_db)

        assert result is mock_db

    @pytest.mark.asyncio
    async def test_raises_503_when_not_configured(self) -> None:
        """Should raise HTTPException 503 when database is not configured."""
        mock_db = AsyncMock()

        with patch("api.dependencies.is_db_configured", return_value=False):
            with pytest.raises(HTTPException) as exc_info:
                await require_db(db=mock_db)

        assert exc_info.value.status_code == 503
        assert "Database not configured" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_error_message_mentions_env_vars(self) -> None:
        """Error message should mention required environment variables."""
        mock_db = AsyncMock()

        with patch("api.dependencies.is_db_configured", return_value=False):
            with pytest.raises(HTTPException) as exc_info:
                await require_db(db=mock_db)

        assert "DATABASE_URL" in exc_info.value.detail
        assert "INSTANCE_CONNECTION_NAME" in exc_info.value.detail


class TestOptionalDb:
    """Tests for optional_db dependency."""

    @pytest.mark.asyncio
    async def test_returns_db_when_configured(self) -> None:
        """Should return db session when database is configured."""
        mock_db = AsyncMock()

        with patch("api.dependencies.is_db_configured", return_value=True):
            result = await optional_db(db=mock_db)

        assert result is mock_db

    @pytest.mark.asyncio
    async def test_returns_none_when_not_configured(self) -> None:
        """Should return None when database is not configured."""
        mock_db = AsyncMock()

        with patch("api.dependencies.is_db_configured", return_value=False):
            result = await optional_db(db=mock_db)

        assert result is None

    @pytest.mark.asyncio
    async def test_does_not_raise_when_not_configured(self) -> None:
        """Should not raise exception when database is not configured."""
        mock_db = AsyncMock()

        with patch("api.dependencies.is_db_configured", return_value=False):
            # Should not raise - just returns None
            result = await optional_db(db=mock_db)
            assert result is None
