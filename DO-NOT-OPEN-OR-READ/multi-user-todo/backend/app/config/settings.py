"""Application settings and configuration."""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = ConfigDict(env_file=".env", case_sensitive=False)

    # Database Configuration
    database_url: str

    # JWT Configuration
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 43200  # 30 days
    jwt_refresh_token_expire_days: int = 90

    # CORS Configuration
    cors_origins: str = "http://localhost:3000"

    # Application Configuration
    app_name: str = "Multi-User Todo Application"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"

    # Security
    secret_key: str

    # Session Configuration
    session_expire_days: int = 90
    single_device_login: bool = True

    # Better Auth Configuration
    better_auth_secret: str
    better_auth_url: str

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()