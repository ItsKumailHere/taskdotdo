"""Error handling middleware and exception handlers."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.utils.errors import AppException
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handle application-specific exceptions.

    Args:
        request: FastAPI request object
        exc: Application exception

    Returns:
        JSON response with error details
    """
    logger.error(
        f"Application error: {exc.message}",
        extra={
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
        },
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """
    Handle database integrity constraint violations.

    Args:
        request: FastAPI request object
        exc: SQLAlchemy IntegrityError

    Returns:
        JSON response with error details
    """
    logger.error(
        f"Database integrity error: {str(exc)}",
        extra={"path": request.url.path},
    )

    # Parse common integrity errors
    error_message = "Database constraint violation"
    if "unique constraint" in str(exc).lower():
        error_message = "A record with this value already exists"
    elif "foreign key constraint" in str(exc).lower():
        error_message = "Referenced record does not exist"

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": error_message,
            "details": {"type": "integrity_error"},
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions.

    Args:
        request: FastAPI request object
        exc: Generic exception

    Returns:
        JSON response with error details
    """
    logger.exception(
        f"Unexpected error: {str(exc)}",
        extra={"path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "details": {"message": str(exc)} if logger.level <= 10 else {},  # Show details in debug mode
        },
    )
