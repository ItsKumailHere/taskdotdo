# Data Model: User Authentication & Authorization

**Feature**: User Authentication & Authorization
**Date**: 2026-01-07

## Database Schema

### Users Table (handled by Better Auth with custom extensions)

The primary user data will be managed by Better Auth, but we'll extend as needed:

```sql
-- Managed by Better Auth
users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Passwords handled separately by Better Auth
-- We may need additional user profile table if extended fields are required
user_profiles (
    user_id VARCHAR(255) REFERENCES users(id),
    bio TEXT,
    avatar_url VARCHAR(500),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sessions Table (if needed for custom session tracking)

```sql
-- Only if we need custom session tracking beyond JWT
sessions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id),
    token_hash VARCHAR(255) NOT NULL,  -- Hash of JWT for revocation
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## SQLModel Definitions

### User Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: str

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: str = Field(default=None, primary_key=True)
    email_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Note: Password is handled by Better Auth
```

### UserProfile Model (extension if needed)

```python
class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"
    
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    bio: Optional[str] = Field(default=None)
    avatar_url: Optional[str] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## JWT Token Structure

### Access Token Payload

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "name": "User Name",
  "exp": 1234567890,
  "iat": 1234567890,
  "type": "access"
}
```

### Refresh Token Payload

```json
{
  "sub": "user_id",
  "jti": "unique-refresh-token-id",
  "exp": 1234567890,
  "type": "refresh"
}
```

### Token Validation

- Verify signature using stored secret
- Check expiration (exp claim)
- Validate issuer (iss claim) if used
- Optionally verify audience (aud claim)

## Relationships

### User to Todos (one-to-many)
- Foreign key: todos.user_id → users.id
- Ensures data isolation between users
- Enables efficient querying of user's todos

## Indexes

### Required Indexes
- users.email (UNIQUE INDEX) - for authentication lookups
- todos.user_id (INDEX) - for filtering user's todos
- todos.completed (INDEX) - for status filtering

## Security Considerations

### Password Storage
- Passwords are handled by Better Auth
- Stored using SHA-256 as specified (though bcrypt would be preferred)
- Never stored in plain text

### Token Security
- JWTs are stateless but have limited lifetime
- Consider refresh tokens for better UX
- Token revocation may require sessions table