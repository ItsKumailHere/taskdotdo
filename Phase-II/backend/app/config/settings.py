from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Authentication configuration
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-min-32-chars-change-this-in-production")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Application configuration
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", True)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: str = "*"  # In production, specify exact origins
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TaskDo API - Phase II"


settings = Settings()