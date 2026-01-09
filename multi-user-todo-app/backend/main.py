from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.todos import router as todos_router
from app.api.v1.categories import router as categories_router
from app.api.v1.tags import router as tags_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.user_preferences import router as user_preferences_router
from app.database.database import engine, async_engine
from app.database.migrations import run_migrations_online
from app.models import user, todo, category, tag, notification, session, user_preferences
from sqlmodel import SQLModel
import logging

# Configure logging
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Runs startup and shutdown logic.
    """
    # Startup
    logger.info("Starting up application...")
    try:
        # Run database migrations
        logger.info("Running database migrations...")
        run_migrations_online()
        logger.info("Database migrations completed")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

    yield  # Application runs here

    # Shutdown
    logger.info("Shutting down application...")
    await async_engine.dispose()  # Properly close async engine
    engine.dispose()  # Properly close sync engine


# Create the FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose the authorization header to the frontend
    expose_headers=["Access-Control-Allow-Origin"]
)

# Include API routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(todos_router, prefix=settings.API_V1_STR)
app.include_router(categories_router, prefix=settings.API_V1_STR)
app.include_router(tags_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)
app.include_router(user_preferences_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Multi-User Todo API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
