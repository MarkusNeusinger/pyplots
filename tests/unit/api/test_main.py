"""
Tests for api/main.py FastAPI endpoints.

Tests the main API endpoints:
- Root endpoint (/)
- Health check (/health)
- Hello endpoint (/hello/{name})
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint (/)."""

    def test_returns_welcome_message(self, client: TestClient) -> None:
        """Root endpoint should return welcome message."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to pyplots API"

    def test_returns_version(self, client: TestClient) -> None:
        """Root endpoint should return version."""
        response = client.get("/")

        data = response.json()
        assert "version" in data
        assert data["version"] == "0.1.0"

    def test_returns_docs_url(self, client: TestClient) -> None:
        """Root endpoint should return docs URL."""
        response = client.get("/")

        data = response.json()
        assert data["docs"] == "/docs"

    def test_returns_health_url(self, client: TestClient) -> None:
        """Root endpoint should return health URL."""
        response = client.get("/")

        data = response.json()
        assert data["health"] == "/health"


class TestHealthEndpoint:
    """Tests for the health check endpoint (/health)."""

    def test_returns_200_status(self, client: TestClient) -> None:
        """Health endpoint should return 200 OK."""
        response = client.get("/health")

        assert response.status_code == 200

    def test_returns_healthy_status(self, client: TestClient) -> None:
        """Health endpoint should report healthy status."""
        response = client.get("/health")

        data = response.json()
        assert data["status"] == "healthy"

    def test_returns_service_name(self, client: TestClient) -> None:
        """Health endpoint should return service name."""
        response = client.get("/health")

        data = response.json()
        assert data["service"] == "pyplots-api"

    def test_returns_version(self, client: TestClient) -> None:
        """Health endpoint should return version."""
        response = client.get("/health")

        data = response.json()
        assert data["version"] == "0.1.0"


class TestHelloEndpoint:
    """Tests for the hello endpoint (/hello/{name})."""

    def test_greets_by_name(self, client: TestClient) -> None:
        """Hello endpoint should greet by name."""
        response = client.get("/hello/World")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello, World!"

    def test_greets_different_names(self, client: TestClient) -> None:
        """Hello endpoint should work with different names."""
        for name in ["Alice", "Bob", "Claude"]:
            response = client.get(f"/hello/{name}")

            assert response.status_code == 200
            data = response.json()
            assert data["message"] == f"Hello, {name}!"

    def test_returns_service_name(self, client: TestClient) -> None:
        """Hello endpoint should return service name."""
        response = client.get("/hello/Test")

        data = response.json()
        assert data["service"] == "pyplots"

    def test_handles_special_characters(self, client: TestClient) -> None:
        """Hello endpoint should handle URL-encoded names."""
        response = client.get("/hello/John%20Doe")

        assert response.status_code == 200
        data = response.json()
        assert "John Doe" in data["message"]

    def test_handles_unicode_names(self, client: TestClient) -> None:
        """Hello endpoint should handle unicode names."""
        response = client.get("/hello/日本語")

        assert response.status_code == 200
        data = response.json()
        assert "日本語" in data["message"]


class TestOpenAPIDocumentation:
    """Tests for OpenAPI documentation endpoints."""

    def test_docs_endpoint_exists(self, client: TestClient) -> None:
        """Swagger docs should be available at /docs."""
        response = client.get("/docs")

        # Swagger UI returns 200
        assert response.status_code == 200

    def test_redoc_endpoint_exists(self, client: TestClient) -> None:
        """ReDoc should be available at /redoc."""
        response = client.get("/redoc")

        assert response.status_code == 200

    def test_openapi_json_exists(self, client: TestClient) -> None:
        """OpenAPI schema should be available at /openapi.json."""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "pyplots API"


class TestCORSMiddleware:
    """Tests for CORS configuration."""

    def test_cors_allows_localhost(self, client: TestClient) -> None:
        """CORS should allow localhost origins for preflight requests."""
        response = client.options(
            "/", headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"}
        )

        # Preflight should succeed with 200 or 204 (not 400 which indicates an error)
        assert response.status_code in [200, 204], f"Preflight failed with status {response.status_code}"

    def test_cors_headers_present(self, client: TestClient) -> None:
        """CORS headers should be present in response for cross-origin requests."""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})

        assert response.status_code == 200
        # Verify CORS headers are present in the response
        cors_header = response.headers.get("access-control-allow-origin")
        assert cors_header is not None, "Missing Access-Control-Allow-Origin header"
        # Should allow the requesting origin or use wildcard
        assert cors_header in ["http://localhost:3000", "*"], f"Unexpected CORS origin: {cors_header}"


class TestAppConfiguration:
    """Tests for app configuration."""

    def test_app_title(self) -> None:
        """App should have correct title."""
        assert app.title == "pyplots API"

    def test_app_version(self) -> None:
        """App should have correct version."""
        assert app.version == "0.1.0"

    def test_app_description(self) -> None:
        """App should have description."""
        assert "AI-powered" in app.description
        assert "plotting" in app.description.lower()


class TestSpecsEndpoint:
    """Tests for the specs endpoint (/specs)."""

    def test_returns_200_status(self, client: TestClient) -> None:
        """Specs endpoint should return 200 OK."""
        response = client.get("/specs")
        assert response.status_code == 200

    def test_returns_specs_list(self, client: TestClient) -> None:
        """Specs endpoint should return a list of specs."""
        response = client.get("/specs")
        data = response.json()
        assert "specs" in data
        assert isinstance(data["specs"], list)

    def test_returns_known_specs(self, client: TestClient) -> None:
        """Specs endpoint should return known spec IDs."""
        response = client.get("/specs")
        data = response.json()
        specs = data["specs"]
        # Should contain some of our known specs
        assert len(specs) > 0
        # Check for at least one known spec
        known_specs = {"scatter-basic", "bar-basic", "box-basic", "histogram-basic", "pie-basic-labeled", "area-basic"}
        assert any(spec in known_specs for spec in specs)

    def test_excludes_template_files(self, client: TestClient) -> None:
        """Specs endpoint should exclude template and versioning files."""
        response = client.get("/specs")
        data = response.json()
        specs = data["specs"]
        assert ".template" not in specs
        assert "VERSIONING" not in specs


class TestSpecImagesEndpoint:
    """Tests for the spec images endpoint (/specs/{spec_id}/images)."""

    def test_returns_200_for_valid_spec(self, client: TestClient) -> None:
        """Images endpoint should return 200 for valid spec."""
        response = client.get("/specs/scatter-basic/images")
        assert response.status_code == 200

    def test_returns_404_for_invalid_spec(self, client: TestClient) -> None:
        """Images endpoint should return 404 for non-existent spec."""
        response = client.get("/specs/nonexistent-spec/images")
        assert response.status_code == 404

    def test_returns_spec_id_in_response(self, client: TestClient) -> None:
        """Images endpoint should return spec_id in response."""
        response = client.get("/specs/scatter-basic/images")
        data = response.json()
        assert data["spec_id"] == "scatter-basic"

    def test_returns_images_list(self, client: TestClient) -> None:
        """Images endpoint should return images list."""
        response = client.get("/specs/scatter-basic/images")
        data = response.json()
        assert "images" in data
        assert isinstance(data["images"], list)

    def test_image_has_library_and_url(self, client: TestClient) -> None:
        """Each image should have library and url fields."""
        response = client.get("/specs/scatter-basic/images")
        data = response.json()
        # If images are available (depends on GCS)
        for img in data["images"]:
            assert "library" in img
            assert "url" in img
