"""Main API v1 router that aggregates all v1 routes."""

from fastapi import APIRouter

# Import route modules
from app.api.v1 import auth, categories, tags, todos

# Create main v1 router
api_router = APIRouter(prefix="/v1")

# Include authentication routes
api_router.include_router(auth.router)

# Include todo management routes
api_router.include_router(todos.router)
api_router.include_router(categories.router)
api_router.include_router(tags.router)


@api_router.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        Status message indicating API is healthy
    """
    return {"status": "healthy", "version": "1.0.0"}
