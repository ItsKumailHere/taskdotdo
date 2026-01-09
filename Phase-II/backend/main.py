from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.v1 import api_router
from app.database.session import async_engine
from app.database.init_db import init_db
from app.utils.logging import setup_logging
import logging

# Configure logging
setup_logging(settings.LOG_LEVEL if hasattr(settings, 'LOG_LEVEL') else 'INFO')
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Runs startup and shutdown logic.
    """
    # Startup
    logger.info("Starting up TaskDo API...")
    await init_db()  # Initialize database tables on startup
    logger.info("Database initialized")

    yield  # Application runs here

    # Shutdown
    logger.info("Shutting down TaskDo API...")
    await async_engine.dispose()


# Create the FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME or "TaskDo API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS.split(",") if isinstance(settings.BACKEND_CORS_ORIGINS, str) else settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {"message": "TaskDo API - Phase II"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )    