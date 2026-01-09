"""CORS middleware configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings


def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the application.

    Allows frontend to make cross-origin requests to the API.

    Args:
        app: FastAPI application instance
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,  # Frontend URLs
        allow_credentials=True,  # Allow cookies and Authorization headers
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],  # Allow all headers (including Authorization)
    )
