"""
API routing structure for the TaskDo backend
"""
from fastapi import APIRouter


# Create main API router
api_router = APIRouter()

# Import and include individual API routers
from . import auth, users, todos

# Include API routes under /api/v1
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])