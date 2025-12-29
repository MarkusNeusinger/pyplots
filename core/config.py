"""
Centralized configuration management using Pydantic Settings.

All environment variables are defined here with type validation,
defaults, and documentation.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Environment variables are loaded from .env file if present.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    # =============================================================================
    # DATABASE
    # =============================================================================

    database_url: Optional[str] = None
    """PostgreSQL connection URL (postgresql+asyncpg://user:pass@host:5432/dbname)"""

    instance_connection_name: Optional[str] = None
    """Cloud SQL instance connection name (for Cloud Run deployment)"""

    db_user: str = "postgres"
    """Database user"""

    db_pass: str = ""
    """Database password"""

    db_name: str = "pyplots"
    """Database name"""

    # =============================================================================
    # GOOGLE CLOUD
    # =============================================================================

    gcs_bucket: str = "pyplots-images"
    """Google Cloud Storage bucket for plot images"""

    google_application_credentials: Optional[str] = None
    """Path to Google Cloud service account credentials JSON"""

    # =============================================================================
    # APPLICATION
    # =============================================================================

    environment: str = "development"
    """Environment: development, staging, or production"""

    base_url: str = "https://pyplots.ai"
    """Base URL for the application (used in sitemaps, etc.)"""

    api_version: str = "0.2.0"
    """API version"""

    # =============================================================================
    # GITHUB
    # =============================================================================

    github_token: Optional[str] = None
    """GitHub personal access token for API access"""

    github_repository: str = "MarkusNeusinger/pyplots"
    """GitHub repository in format owner/repo"""

    # =============================================================================
    # API KEYS (for AI services)
    # =============================================================================

    anthropic_api_key: Optional[str] = None
    """Anthropic API key for Claude"""

    openai_api_key: Optional[str] = None
    """OpenAI API key"""

    google_ai_api_key: Optional[str] = None
    """Google AI API key for Gemini"""

    # =============================================================================
    # CACHE
    # =============================================================================

    cache_ttl: int = 600
    """Cache TTL in seconds (default: 10 minutes)"""

    cache_maxsize: int = 1000
    """Maximum number of cache entries"""

    # =============================================================================
    # CORS
    # =============================================================================

    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "https://pyplots.ai",
        "https://www.pyplots.ai",
    ]
    """Allowed CORS origins"""

    # =============================================================================
    # HELPER METHODS
    # =============================================================================

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"

    @property
    def is_test(self) -> bool:
        """Check if running in test environment."""
        return self.environment.lower() == "test"

    @property
    def is_database_configured(self) -> bool:
        """
        Check if database configuration is present.

        Note: This only verifies config presence, not connectivity or validity.
        Use core.database.is_db_configured() for runtime checks.
        """
        return bool(self.database_url or self.instance_connection_name)

    @property
    def has_google_cloud(self) -> bool:
        """Check if Google Cloud is configured."""
        return bool(self.google_application_credentials or self.instance_connection_name)


# Global settings instance
# Import this from other modules: from core.config import settings
settings = Settings()
