from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from passlib.context import CryptContext
import enum


# Password hashing context
# Using bcrypt as primary, with fallback options if bcrypt has issues
pwd_context = CryptContext(
    schemes=["bcrypt", "argon2", "pbkdf2_sha256"],
    deprecated="auto",
    bcrypt__rounds=12,
    argon2__rounds=10,
    argon2__memory_cost=1024,
    pbkdf2_sha256__default_rounds=29000
)


class UserRole(str, enum.Enum):
    """User roles for authorization"""
    USER = "user"
    ADMIN = "admin"


class UserBase(SQLModel):
    """Base model for user with common fields"""
    email: str = Field(unique=True, index=True)
    name: str = Field(min_length=1)
    role: UserRole = Field(default=UserRole.USER)


class User(UserBase, table=True):
    """User model for the database"""
    __tablename__ = "users"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str = Field(min_length=1)
    hashed_password: str = Field(min_length=1)
    role: UserRole = Field(default=UserRole.USER)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Whether the user's email is verified
    is_verified: bool = Field(default=False)
    
    # Whether the user account is active
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(min_length=8)
    

class UserUpdate(SQLModel):
    """Schema for updating user information"""
    name: Optional[str] = Field(default=None, min_length=1)
    email: Optional[str] = Field(default=None, unique=True, index=True)
    password: Optional[str] = Field(default=None, min_length=8)


class UserPublic(UserBase):
    """Public representation of a user (without sensitive data)"""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_verified: bool = False
    is_active: bool = True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a hash for a plain password"""
    # Ensure password is properly truncated to 72 bytes to comply with bcrypt limits
    # First encode to bytes to measure actual byte length, then truncate if needed
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes and decode back to string
        truncated_bytes = password_bytes[:72]
        truncated_password = truncated_bytes.decode('utf-8', errors='ignore')
    else:
        truncated_password = password

    # Double check the length before sending to bcrypt
    final_password = truncated_password[:72] if len(truncated_password.encode('utf-8')) > 72 else truncated_password

    try:
        return pwd_context.hash(final_password)
    except ValueError as e:
        if "password cannot be longer than 72 bytes" in str(e):
            # If bcrypt still complains, ensure we're sending exactly 72 chars
            # This might happen due to multibyte characters
            safe_password = final_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            # Try to use a different algorithm explicitly
            return pwd_context.hash(safe_password, scheme="pbkdf2_sha256")
        else:
            raise e