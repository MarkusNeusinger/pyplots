"""
Standardized exception handling for pyplots API.

Provides consistent error responses and HTTP status codes.
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# ===== Error Response Schemas =====


class ErrorDetail(BaseModel):
    """Standard error detail format."""

    error: str
    detail: str
    path: str | None = None


class ErrorResponse(BaseModel):
    """Standard error response format."""

    status: int
    message: str
    errors: list[ErrorDetail] | None = None


# ===== Custom Exceptions =====


class PyplotsException(Exception):
    """Base exception for pyplots API."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ResourceNotFoundError(PyplotsException):
    """Resource not found (404)."""

    def __init__(self, resource: str, identifier: str):
        message = f"{resource} '{identifier}' not found"
        super().__init__(message, status_code=404)
        self.resource = resource
        self.identifier = identifier


class DatabaseNotConfiguredError(PyplotsException):
    """Database not configured (503)."""

    def __init__(self):
        message = "Database not configured. Please set DATABASE_URL or INSTANCE_CONNECTION_NAME environment variable."
        super().__init__(message, status_code=503)


class ExternalServiceError(PyplotsException):
    """External service failure (502)."""

    def __init__(self, service: str, detail: str):
        message = f"External service '{service}' error: {detail}"
        super().__init__(message, status_code=502)
        self.service = service


class ValidationError(PyplotsException):
    """Validation error (400)."""

    def __init__(self, detail: str):
        super().__init__(f"Validation failed: {detail}", status_code=400)


# ===== Exception Handlers =====


async def pyplots_exception_handler(request: Request, exc: PyplotsException) -> JSONResponse:
    """Handle PyplotsException and return standardized JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": exc.status_code, "message": exc.message, "path": request.url.path},
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTPException with standardized format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": exc.status_code, "message": exc.detail, "path": request.url.path},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions with 500 status."""
    return JSONResponse(
        status_code=500,
        content={"status": 500, "message": "Internal server error", "detail": str(exc), "path": request.url.path},
    )


# ===== Helper Functions =====


def raise_not_found(resource: str, identifier: str) -> None:
    """
    Raise a standardized 404 error.

    Args:
        resource: Resource type (e.g., "Spec", "Library")
        identifier: Resource identifier

    Raises:
        ResourceNotFoundError: Always raises
    """
    raise ResourceNotFoundError(resource, identifier)


def raise_database_not_configured() -> None:
    """
    Raise a standardized 503 error for unconfigured database.

    Raises:
        DatabaseNotConfiguredError: Always raises
    """
    raise DatabaseNotConfiguredError()


def raise_external_service_error(service: str, detail: str) -> None:
    """
    Raise a standardized 502 error for external service failures.

    Args:
        service: Service name (e.g., "GCS", "GitHub API")
        detail: Error details

    Raises:
        ExternalServiceError: Always raises
    """
    raise ExternalServiceError(service, detail)


def raise_validation_error(detail: str) -> None:
    """
    Raise a standardized 400 error for validation failures.

    Args:
        detail: Validation error details

    Raises:
        ValidationError: Always raises
    """
    raise ValidationError(detail)
