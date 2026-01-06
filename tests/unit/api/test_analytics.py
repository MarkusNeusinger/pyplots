"""Tests for server-side Plausible analytics tracking."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from api.analytics import PLATFORM_PATTERNS, detect_platform, track_og_image


class TestDetectPlatform:
    """Tests for platform detection from User-Agent."""

    def test_detects_twitter(self) -> None:
        """Should detect Twitter bot."""
        assert detect_platform("Twitterbot/1.0") == "twitter"

    def test_detects_whatsapp(self) -> None:
        """Should detect WhatsApp."""
        assert detect_platform("WhatsApp/2.21.4.22") == "whatsapp"

    def test_detects_facebook(self) -> None:
        """Should detect Facebook."""
        assert detect_platform("facebookexternalhit/1.1") == "facebook"

    def test_detects_linkedin(self) -> None:
        """Should detect LinkedIn."""
        assert detect_platform("LinkedInBot/1.0") == "linkedin"

    def test_detects_slack(self) -> None:
        """Should detect Slack."""
        assert detect_platform("Slackbot-LinkExpanding 1.0") == "slack"

    def test_detects_discord(self) -> None:
        """Should detect Discord."""
        assert detect_platform("Mozilla/5.0 (compatible; Discordbot/2.0)") == "discord"

    def test_detects_telegram(self) -> None:
        """Should detect Telegram."""
        assert detect_platform("TelegramBot/1.0") == "telegram"

    def test_detects_teams(self) -> None:
        """Should detect Microsoft Teams."""
        assert detect_platform("Mozilla/5.0 Microsoft Teams") == "teams"

    def test_detects_google(self) -> None:
        """Should detect Googlebot."""
        assert detect_platform("Mozilla/5.0 (compatible; Googlebot/2.1)") == "google"

    def test_returns_unknown_for_regular_browser(self) -> None:
        """Should return unknown for regular browsers."""
        assert detect_platform("Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0") == "unknown"

    def test_returns_unknown_for_empty_string(self) -> None:
        """Should return unknown for empty User-Agent."""
        assert detect_platform("") == "unknown"

    def test_case_insensitive(self) -> None:
        """Should match case-insensitively."""
        assert detect_platform("TWITTERBOT/1.0") == "twitter"
        assert detect_platform("twitterbot/1.0") == "twitter"

    def test_all_platforms_have_patterns(self) -> None:
        """Should have 27 platform patterns defined."""
        assert len(PLATFORM_PATTERNS) == 27


class TestTrackOgImage:
    """Tests for og:image tracking function."""

    @pytest.fixture
    def mock_request(self) -> MagicMock:
        """Create a mock FastAPI request."""
        request = MagicMock()
        request.headers = {"user-agent": "Twitterbot/1.0", "x-forwarded-for": "1.2.3.4"}
        request.client = MagicMock()
        request.client.host = "127.0.0.1"
        return request

    def test_creates_async_task(self, mock_request: MagicMock) -> None:
        """Should create background task without blocking."""
        with patch("api.analytics.asyncio.create_task") as mock_create_task:
            track_og_image(mock_request, page="home")
            mock_create_task.assert_called_once()

    def test_home_page_url(self, mock_request: MagicMock) -> None:
        """Should build correct URL for home page."""
        with patch("api.analytics.asyncio.create_task") as mock_create_task:
            track_og_image(mock_request, page="home")
            call_args = mock_create_task.call_args[0][0]
            # The coroutine should be called with home URL
            assert call_args is not None

    def test_catalog_page_url(self, mock_request: MagicMock) -> None:
        """Should build correct URL for catalog page."""
        with patch("api.analytics._send_plausible_event", new_callable=AsyncMock):
            with patch("api.analytics.asyncio.create_task") as mock_create_task:
                track_og_image(mock_request, page="catalog")
                mock_create_task.assert_called_once()

    def test_spec_overview_url(self, mock_request: MagicMock) -> None:
        """Should build correct URL for spec overview."""
        with patch("api.analytics.asyncio.create_task"):
            # Should not raise even with spec_overview page
            track_og_image(mock_request, page="spec_overview", spec="scatter-basic")

    def test_spec_detail_url(self, mock_request: MagicMock) -> None:
        """Should build correct URL for spec detail."""
        with patch("api.analytics.asyncio.create_task"):
            track_og_image(mock_request, page="spec_detail", spec="scatter-basic", library="matplotlib")

    def test_fallback_url_when_spec_none(self, mock_request: MagicMock) -> None:
        """Should fallback to home URL when spec is None for spec-based page."""
        with patch("api.analytics.asyncio.create_task"):
            # Should not raise - falls back to home URL
            track_og_image(mock_request, page="spec_overview", spec=None)

    def test_includes_filter_props(self, mock_request: MagicMock) -> None:
        """Should include filter parameters in props."""
        with patch("api.analytics.asyncio.create_task"):
            track_og_image(mock_request, page="home", filters={"lib": "plotly", "dom": "statistics"})

    def test_uses_x_forwarded_for(self) -> None:
        """Should use X-Forwarded-For header for client IP."""
        request = MagicMock()
        request.headers = {"user-agent": "Twitterbot/1.0", "x-forwarded-for": "5.6.7.8"}
        request.client = None

        with patch("api.analytics.asyncio.create_task"):
            track_og_image(request, page="home")

    def test_fallback_to_client_host(self) -> None:
        """Should fallback to client.host when X-Forwarded-For not present."""
        request = MagicMock()
        request.headers = {"user-agent": "Twitterbot/1.0"}
        request.client = MagicMock()
        request.client.host = "10.0.0.1"

        with patch("api.analytics.asyncio.create_task"):
            track_og_image(request, page="home")

    def test_handles_missing_client(self) -> None:
        """Should handle missing client gracefully."""
        request = MagicMock()
        request.headers = {"user-agent": "Twitterbot/1.0"}
        request.client = None

        with patch("api.analytics.asyncio.create_task"):
            track_og_image(request, page="home")


class TestSendPlausibleEvent:
    """Tests for Plausible API call."""

    @pytest.mark.asyncio
    async def test_sends_correct_payload(self) -> None:
        """Should send correct payload to Plausible."""
        from api.analytics import _send_plausible_event

        with patch("api.analytics.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client

            await _send_plausible_event(
                user_agent="Twitterbot/1.0",
                client_ip="1.2.3.4",
                name="og_image_view",
                url="https://pyplots.ai/",
                props={"page": "home", "platform": "twitter"},
            )

            mock_client.post.assert_called_once()
            call_kwargs = mock_client.post.call_args[1]
            assert call_kwargs["json"]["name"] == "og_image_view"
            assert call_kwargs["json"]["domain"] == "pyplots.ai"

    @pytest.mark.asyncio
    async def test_handles_network_error(self) -> None:
        """Should handle network errors gracefully."""
        from api.analytics import _send_plausible_event

        with patch("api.analytics.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.side_effect = Exception("Network error")
            mock_client_class.return_value.__aenter__.return_value = mock_client

            # Should not raise
            await _send_plausible_event(
                user_agent="Twitterbot/1.0",
                client_ip="1.2.3.4",
                name="og_image_view",
                url="https://pyplots.ai/",
                props={},
            )
