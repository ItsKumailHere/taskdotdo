# Quickstart Guide: User Authentication & Authorization

**Feature**: User Authentication & Authorization
**Date**: 2026-01-07

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or Neon Serverless Postgres)
- Next.js 16+

## Setup Instructions

### Backend Setup (FastAPI)

1. Install dependencies:
```bash
pip install fastapi sqlmodel python-jose[cryptography] passlib[bcrypt] python-multipart
```

2. Configure database connection:
```python
# In db.py
from sqlmodel import create_engine

DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
```

3. Set up authentication utilities:
```python
# In auth_utils.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt

pwd_context = CryptContext(schemes=["sha256"], deprecated="auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Frontend Setup (Next.js 16)

1. Install Better Auth:
```bash
npm install better-auth
```

2. Initialize Better Auth in your Next.js app:
```javascript
// In lib/auth-client.ts
import { initClient } from "better-auth/client";
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  // Configuration options
});
```

3. Set up protected routes:
```typescript
// In components/auth/ProtectedRoute.tsx
import { useAuth } from "better-auth/react";
import { useRouter } from "next/router";
import { useEffect } from "react";

export const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading || !isAuthenticated) {
    return <div>Loading...</div>;
  }

  return <>{children}</>;
};
```

## Running the Application

### Backend
```bash
cd backend
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

## Key Endpoints

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate a user
- `POST /api/auth/logout` - Log out a user
- `GET /api/auth/me` - Get current user info

## Testing Authentication

1. Register a new user:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "name": "Test User"}'
```

2. Login to get JWT token:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

3. Access protected endpoint:
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```