"""Custom exception classes for application-specific errors."""

from typing import Any, Optional


class AppException(Exception):
    """Base exception class for all application exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(AppException):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found", details: Optional[dict[str, Any]] = None):
        super().__init__(message=message, status_code=404, details=details)


class UnauthorizedException(AppException):
    """Exception raised when authentication fails."""

    def __init__(
        self, message: str = "Unauthorized access", details: Optional[dict[str, Any]] = None
    ):
        super().__init__(message=message, status_code=401, details=details)


class ForbiddenException(AppException):
    """Exception raised when access is forbidden."""

    def __init__(
        self,
        message: str = "Access forbidden",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=403, details=details)


class BadRequestException(AppException):
    """Exception raised for invalid request data."""

    def __init__(
        self,
        message: str = "Invalid request data",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=400, details=details)


class ConflictException(AppException):
    """Exception raised when a resource conflict occurs."""

    def __init__(
        self,
        message: str = "Resource conflict",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=409, details=details)
