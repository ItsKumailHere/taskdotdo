"""Password hashing and verification utilities using bcrypt."""

import hashlib
import bcrypt

from passlib.context import CryptContext

# Password hashing context using a PBKDF2 scheme for new hashes.
# Keep bcrypt out of the default scheme to avoid triggering backend
# initialization that can error on long inputs. Legacy bcrypt hashes
# are verified explicitly with the `bcrypt` module below.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def _prepare_password(password: str) -> str:
    """
    Prepare password for bcrypt by hashing with SHA-256 first.

    This allows passwords of any length, bypassing bcrypt's 72-byte limit.

    Args:
        password: Plain text password

    Returns:
        Hex-encoded SHA-256 hash of password
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256 + bcrypt.

    First hashes the password with SHA-256 to handle any length,
    then applies bcrypt for secure password storage.

    Args:
        password: Plain text password to hash (any length)

    Returns:
        Hashed password string

    Example:
        >>> hashed = hash_password("mySecurePassword123!")
        >>> print(hashed)
        $2b$12$...
    """
    prepared = _prepare_password(password)
    return pwd_context.hash(prepared)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Supports both old (direct bcrypt) and new (SHA-256 + bcrypt) methods
    for backwards compatibility during migration.

    Args:
        plain_password: Plain text password to verify (any length)
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("myPassword")
        >>> verify_password("myPassword", hashed)
        True
        >>> verify_password("wrongPassword", hashed)
        False
    """
    # Try new method (SHA-256 + pbkdf2) first
    try:
        prepared = _prepare_password(plain_password)
        if pwd_context.verify(prepared, hashed_password):
            return True
    except Exception:
        pass

    # Fallback to old method (direct bcrypt) for existing users.
    # Use the bcrypt library directly and treat ValueError (too-long
    # passwords) as a non-match.
    try:
        # hashed_password is expected to be a bcrypt hash string (e.g. $2b$...)
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        # bcrypt raises ValueError for passwords >72 bytes; treat as non-match
        return False
    except Exception:
        return False

    return False
