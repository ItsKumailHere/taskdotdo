"""Main FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from app.api.v1.router import api_router
from app.config.settings import settings
from app.database.database import init_db
from app.middleware.cors import setup_cors
from app.middleware.error_handler import (
    app_exception_handler,
    generic_exception_handler,
    integrity_error_handler,
)
from app.utils.errors import AppException
from app.utils.logger import get_logger, setup_logging

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")

    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Multi-user todo application API with authentication and organization features",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,  # Disable docs in production
    redoc_url="/redoc" if settings.debug else None,
)

# Setup CORS
setup_cors(app)

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include API routers
app.include_router(api_router, prefix="/api")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs" if settings.debug else "disabled",
    }


# Health check endpoint (outside /api for load balancers)
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )
