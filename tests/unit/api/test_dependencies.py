"""
Tests for api/dependencies.py.

Tests the reusable FastAPI dependencies for database access.
"""

from unittest.mock import AsyncMock, patch

import pytest

from api.dependencies import optional_db, require_db
from api.exceptions import DatabaseNotConfiguredError


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
        """Should raise DatabaseNotConfiguredError when database is not configured."""
        mock_db = AsyncMock()

        with patch("api.dependencies.is_db_configured", return_value=False):
            with pytest.raises(DatabaseNotConfiguredError) as exc_info:
                await require_db(db=mock_db)

        assert exc_info.value.status_code == 503
        assert "Database not configured" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_error_message_mentions_env_vars(self) -> None:
        """Error message should mention required environment variables."""
        mock_db = AsyncMock()

        with patch("api.dependencies.is_db_configured", return_value=False):
            with pytest.raises(DatabaseNotConfiguredError) as exc_info:
                await require_db(db=mock_db)

        error_message = str(exc_info.value)
        assert "DATABASE_URL" in error_message
        assert "INSTANCE_CONNECTION_NAME" in error_message


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
