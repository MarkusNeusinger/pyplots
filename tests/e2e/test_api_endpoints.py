"""
End-to-end tests for API endpoints.

Tests full stack with real database and FastAPI TestClient.
Covers complete request-response cycle through all layers.
"""

from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app


pytestmark = pytest.mark.e2e


@pytest.fixture
async def async_client():
    """Create async test client for FastAPI."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


class TestSpecsEndpoints:
    """Integration tests for /specs endpoints."""

    async def test_get_specs_with_db(self, async_client, test_db_with_data):
        """Should return all specs from database."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/specs")

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]["id"] in ["scatter-basic", "bar-grouped"]

    async def test_get_spec_detail(self, async_client, test_db_with_data):
        """Should return spec detail with implementations."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/specs/scatter-basic")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "scatter-basic"
            assert data["title"] == "Basic Scatter Plot"
            assert "impls" in data
            assert len(data["impls"]) == 2

    async def test_get_spec_not_found(self, async_client, test_db_with_data):
        """Should return 404 for non-existent spec."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/specs/nonexistent")

            assert response.status_code == 404

    async def test_get_spec_images(self, async_client, test_db_with_data):
        """Should return images for spec."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/specs/scatter-basic/images")

            assert response.status_code == 200
            data = response.json()
            assert "images" in data
            assert len(data["images"]) == 2


class TestLibrariesEndpoints:
    """Integration tests for /libraries endpoints."""

    async def test_get_libraries(self, async_client, test_db_with_data):
        """Should return all libraries."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/libraries")

            assert response.status_code == 200
            data = response.json()
            assert "libraries" in data
            assert len(data["libraries"]) == 2

    async def test_get_library_images(self, async_client, test_db_with_data):
        """Should return images for library."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/libraries/matplotlib/images")

            assert response.status_code == 200
            data = response.json()
            assert "images" in data
            assert len(data["images"]) == 2

    async def test_get_library_images_invalid(self, async_client, test_db_with_data):
        """Should return 404 for invalid library."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/libraries/invalid/images")

            assert response.status_code == 404


class TestStatsEndpoints:
    """Integration tests for /stats endpoint."""

    async def test_get_stats(self, async_client, test_db_with_data):
        """Should return statistics from database."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/stats")

            assert response.status_code == 200
            data = response.json()
            assert data["specs"] == 2
            assert data["plots"] == 3  # 2 scatter + 1 bar
            assert data["libraries"] == 2


class TestPlotsFilterEndpoints:
    """Integration tests for /plots/filter endpoint."""

    async def test_filter_no_params(self, async_client, test_db_with_data):
        """Should return all images when no filters."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/plots/filter")

            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 3
            assert len(data["images"]) == 3

    async def test_filter_by_library(self, async_client, test_db_with_data):
        """Should filter by library."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/plots/filter?lib=matplotlib")

            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 2  # scatter-matplotlib + bar-matplotlib
            assert all(img["library"] == "matplotlib" for img in data["images"])

    async def test_filter_by_spec(self, async_client, test_db_with_data):
        """Should filter by spec."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/plots/filter?spec=scatter-basic")

            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 2  # scatter-matplotlib + scatter-seaborn
            assert all(img["spec_id"] == "scatter-basic" for img in data["images"])

    async def test_filter_by_plot_type(self, async_client, test_db_with_data):
        """Should filter by plot type tag."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/plots/filter?plot=scatter")

            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 2

    async def test_filter_combined(self, async_client, test_db_with_data):
        """Should filter by multiple parameters (AND logic)."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/plots/filter?lib=matplotlib&plot=scatter")

            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 1  # Only scatter-matplotlib
            assert data["images"][0]["library"] == "matplotlib"
            assert data["images"][0]["spec_id"] == "scatter-basic"


class TestDownloadEndpoints:
    """Integration tests for /download endpoint."""

    async def test_download_code(self, async_client, test_db_with_data):
        """Should return implementation code as Python file."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/download/scatter-basic/matplotlib")

            assert response.status_code == 200
            assert response.headers["content-type"] == "text/x-python; charset=utf-8"
            assert "scatter-basic-matplotlib.py" in response.headers["content-disposition"]

    async def test_download_spec_not_found(self, async_client, test_db_with_data):
        """Should return 404 for non-existent spec."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/download/nonexistent/matplotlib")

            assert response.status_code == 404

    async def test_download_impl_not_found(self, async_client, test_db_with_data):
        """Should return 404 for non-existent implementation."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/download/scatter-basic/plotly")

            assert response.status_code == 404


class TestSeoEndpoints:
    """Integration tests for SEO endpoints."""

    async def test_sitemap(self, async_client, test_db_with_data):
        """Should return sitemap XML with spec URLs."""
        with (
            patch("api.dependencies.get_db", return_value=test_db_with_data),
            patch("api.dependencies.is_db_configured", return_value=True),
        ):
            response = await async_client.get("/sitemap.xml")

            assert response.status_code == 200
            assert response.headers["content-type"] == "application/xml"
            content = response.text
            assert "scatter-basic" in content
            assert "bar-grouped" in content

    async def test_robots_txt(self, async_client):
        """Should return robots.txt."""
        response = await async_client.get("/robots.txt")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
        assert "Sitemap:" in response.text


class TestHealthEndpoints:
    """Integration tests for health endpoints."""

    async def test_root(self, async_client):
        """Should return API info."""
        response = await async_client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to pyplots API"
        assert "version" in data

    async def test_health_check(self, async_client):
        """Should return healthy status."""
        response = await async_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "pyplots-api"

    async def test_hello(self, async_client):
        """Should return personalized greeting."""
        response = await async_client.get("/hello/World")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello, World!"
