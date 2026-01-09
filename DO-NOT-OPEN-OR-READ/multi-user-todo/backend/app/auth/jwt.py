"""JWT token creation and verification utilities."""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from uuid import UUID

from jose import JWTError, jwt

from app.config.settings import settings


def create_access_token(
    subject: str | UUID,
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[dict[str, Any]] = None,
) -> str:
    """
    Create a JWT access token.

    Args:
        subject: Subject of the token (typically user ID)
        expires_delta: Optional custom expiration time
        additional_claims: Optional additional claims to include in token

    Returns:
        Encoded JWT token string

    Example:
        >>> token = create_access_token(subject="user-id-123")
        >>> token = create_access_token(
        ...     subject="user-id-123",
        ...     expires_delta=timedelta(hours=1),
        ...     additional_claims={"email": "user@example.com"}
        ... )
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )

    # Convert UUID to string if necessary
    sub = str(subject) if isinstance(subject, UUID) else subject

    # Build token payload
    to_encode = {
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "sub": sub,
    }

    # Add any additional claims
    if additional_claims:
        to_encode.update(additional_claims)

    # Encode token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token string to decode

    Returns:
        Decoded token payload as dictionary

    Raises:
        JWTError: If token is invalid, expired, or cannot be decoded

    Example:
        >>> token = create_access_token(subject="user-123")
        >>> payload = decode_access_token(token)
        >>> print(payload["sub"])
        user-123
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError as e:
        raise JWTError(f"Could not validate token: {str(e)}")


def verify_token_exp(payload: dict[str, Any]) -> bool:
    """
    Verify that a token has not expired.

    Args:
        payload: Decoded JWT payload

    Returns:
        True if token is still valid, False if expired

    Example:
        >>> payload = decode_access_token(token)
        >>> if verify_token_exp(payload):
        ...     print("Token is valid")
    """
    exp = payload.get("exp")
    if exp is None:
        return False

    return datetime.fromtimestamp(exp, tz=timezone.utc) > datetime.now(timezone.utc)
