"""
Error handling and logging infrastructure for the TaskDo backend
"""
import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
import traceback


# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)


def setup_logging(log_level: str = "INFO"):
    """
    Set up logging configuration for the application
    """
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        logs_dir / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Get root logger and configure it
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Add handlers if not already added
    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)


# Set up logging
setup_logging()


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name
    """
    return logging.getLogger(name)


# Create a logger for this module
logger = get_logger(__name__)


class AppException(HTTPException):
    """
    Base exception class for application-specific errors
    """
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code or f"ERR_{status_code}"


class ValidationError(AppException):
    """
    Exception raised for validation errors
    """
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )


class ResourceNotFoundError(AppException):
    """
    Exception raised when a requested resource is not found
    """
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_type} with ID {resource_id} not found",
            error_code="RESOURCE_NOT_FOUND"
        )


class UnauthorizedError(AppException):
    """
    Exception raised when authentication/authorization fails
    """
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="UNAUTHORIZED"
        )


class ForbiddenError(AppException):
    """
    Exception raised when access is forbidden
    """
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="FORBIDDEN"
        )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for the application
    """
    # Log the full exception with traceback
    logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
    
    # Handle specific exception types
    if isinstance(exc, AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.detail,
                    "path": str(request.url),
                    "timestamp": __import__('datetime').datetime.utcnow().isoformat()
                }
            }
        )
    
    # Handle FastAPI HTTPExceptions
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": f"ERR_{exc.status_code}",
                    "message": exc.detail,
                    "path": str(request.url),
                    "timestamp": __import__('datetime').datetime.utcnow().isoformat()
                }
            }
        )
    
    # Handle all other exceptions
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "path": str(request.url),
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }
        }
    )


def log_api_call(endpoint: str, method: str, user_id: str = None):
    """
    Decorator to log API calls
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            logger.info(f"API Call: {method} {endpoint} - User: {user_id or 'Anonymous'}")
            try:
                result = await func(*args, **kwargs)
                logger.info(f"API Call Success: {method} {endpoint}")
                return result
            except Exception as e:
                logger.error(f"API Call Failed: {method} {endpoint} - Error: {str(e)}")
                raise
        return wrapper
    return decorator


# Initialize logger
logger.info("Logging infrastructure initialized")