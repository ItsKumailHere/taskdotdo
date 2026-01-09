---
name: better-auth-jwt
description: Expert in Better Auth setup for Next.js 16 with JWT token flow. Covers frontend authentication (hooks, signIn/signOut), backend JWT verification in FastAPI, token structure, and secure configuration. Use for all authentication implementations.
---

# Better Auth JWT - Full-Stack Authentication

You are an expert in Better Auth, a modern authentication library for Next.js. This skill covers the complete JWT authentication flow from frontend token generation to backend verification, specifically for Next.js 16 App Router + FastAPI backends.

## Core Philosophy

**Better Auth = Modern Auth + Type Safety + JWT Tokens**

- **Frontend**: Better Auth generates and manages JWT tokens
- **Backend**: FastAPI verifies JWT tokens with shared secret
- **Security**: User isolation enforced at every API call
- **Developer Experience**: Type-safe hooks and utilities

## When to Use This Skill

✅ **Use this skill for:**
- Setting up Better Auth in Next.js 16 App Router
- Configuring JWT token generation and claims
- Implementing login/logout flows on frontend
- Verifying JWT tokens in FastAPI backend
- Managing authentication state with React hooks
- Configuring environment variables and secrets
- Protecting routes (both frontend and backend)

❌ **Don't use for:**
- Basic JWT concepts - you understand tokens
- General authentication theory - fundamental knowledge
- HTTP header formats - standard knowledge

## Authentication Flow Overview

```
┌─────────────────────────────────────────────────────────┐
│ 1. User Login (Frontend - Next.js)                     │
│    ↓                                                    │
│    Better Auth validates credentials                    │
│    ↓                                                    │
│    Generates JWT token with user_id in payload         │
│    ↓                                                    │
│    Returns token to client (stored in memory/cookies)  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. API Request (Frontend → Backend)                    │
│    ↓                                                    │
│    Client includes token in Authorization header       │
│    Authorization: Bearer <jwt_token>                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Token Verification (Backend - FastAPI)              │
│    ↓                                                    │
│    Extract token from Authorization header             │
│    ↓                                                    │
│    Verify signature using BETTER_AUTH_SECRET           │
│    ↓                                                    │
│    Decode payload to get user_id                       │
│    ↓                                                    │
│    Load user from database                             │
│    ↓                                                    │
│    Execute endpoint with authenticated user            │
└─────────────────────────────────────────────────────────┘
```

## Part 1: Frontend Setup (Next.js 16)

### 1. Installation

```bash
npm install better-auth
# or
pnpm add better-auth
# or
yarn add better-auth
```

### 2. Configuration File

Create `lib/auth.ts`:

```typescript
import { betterAuth } from "better-auth"
import { nextCookies } from "better-auth/next-js"

export const auth = betterAuth({
  database: {
    // Not needed for JWT-only auth
    // Better Auth handles user data via your backend
  },
  
  // Email & Password provider
  emailAndPassword: {
    enabled: true,
  },
  
  // JWT configuration
  secret: process.env.BETTER_AUTH_SECRET!,
  
  // Session configuration
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
    updateAge: 60 * 60 * 24, // Update every 24 hours
  },
  
  // Plugins
  plugins: [nextCookies()],
})
```

**Key Concepts:**
- `BETTER_AUTH_SECRET` must match between frontend and backend
- `expiresIn` controls token lifetime
- `emailAndPassword` enables basic auth (can add OAuth providers later)
- `nextCookies()` plugin handles cookie-based session storage

### 3. API Route Handler

Create `app/api/auth/[...all]/route.ts`:

```typescript
import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

export const { GET, POST } = toNextJsHandler(auth)
```

**Key Concepts:**
- Handles all Better Auth endpoints: `/api/auth/sign-in`, `/api/auth/sign-out`, etc.
- Next.js 16 App Router route handler pattern
- Automatically generates all necessary auth endpoints

### 4. Environment Variables

Create `.env.local`:

```bash
# Better Auth Secret (MUST match backend)
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars

# Optional: Database URL if using Better Auth's built-in user management
# DATABASE_URL=postgresql://...

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

**Security Notes:**
- Use a strong, random secret (min 32 characters)
- Never commit secrets to git
- Same secret must be used in backend for JWT verification

### 5. Auth Client (React Hooks)

Create `lib/auth-client.ts`:

```typescript
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000",
})

// Export hooks for use in components
export const { useSession, signIn, signOut, signUp } = authClient
```

**Available Hooks:**
- `useSession()` - Get current session/user state
- `signIn()` - Sign in with email/password
- `signOut()` - Sign out and clear session
- `signUp()` - Create new account

### 6. Using Auth Hooks in Components

```typescript
"use client"

import { useSession, signIn, signOut } from "@/lib/auth-client"
import { useState } from "react"

export function LoginForm() {
  const { data: session, isPending } = useSession()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    const result = await signIn.email({
      email,
      password,
    })

    if (result.error) {
      setError(result.error.message)
    }
  }

  if (isPending) {
    return <div>Loading...</div>
  }

  if (session) {
    return (
      <div>
        <p>Welcome, {session.user.email}!</p>
        <button onClick={() => signOut()}>Sign Out</button>
      </div>
    )
  }

  return (
    <form onSubmit={handleSignIn}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      <button type="submit">Sign In</button>
      {error && <p className="error">{error}</p>}
    </form>
  )
}
```

**Key Concepts:**
- `useSession()` returns `{ data: session, isPending }`
- `session.user` contains user data (email, id, etc.)
- `signIn.email()` for email/password auth
- `signOut()` clears session and removes tokens

### 7. Making Authenticated API Calls

```typescript
"use client"

import { useSession } from "@/lib/auth-client"
import { useEffect, useState } from "react"

export function TodoList() {
  const { data: session } = useSession()
  const [todos, setTodos] = useState([])

  useEffect(() => {
    async function fetchTodos() {
      if (!session?.session.token) return

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/todos`, {
        headers: {
          "Authorization": `Bearer ${session.session.token}`,
          "Content-Type": "application/json",
        },
      })

      if (response.ok) {
        const data = await response.json()
        setTodos(data)
      }
    }

    fetchTodos()
  }, [session])

  return (
    <div>
      {todos.map(todo => (
        <div key={todo.id}>{todo.title}</div>
      ))}
    </div>
  )
}
```

**Key Concepts:**
- Get token from `session.session.token`
- Include in `Authorization: Bearer <token>` header
- Backend verifies token and returns user-specific data

## Part 2: Backend Setup (FastAPI)

### 1. Installation

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

### 2. JWT Verification Dependency

Create `app/auth.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import get_session
from app.models import User
import os

# Security scheme
security = HTTPBearer()

# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable not set")

ALGORITHM = "HS256"

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Verify Better Auth JWT token and return current user.
    
    The token is generated by Better Auth on the frontend and includes
    the user ID in the 'sub' (subject) claim.
    
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    token = credentials.credentials
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token using shared secret
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        # Extract user_id from 'sub' claim
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError as e:
        print(f"JWT decode error: {e}")
        raise credentials_exception
    
    # Get user from database
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    user = result.first()
    
    if user is None:
        raise credentials_exception
    
    return user
```

**Key Concepts:**
- `HTTPBearer` extracts token from `Authorization` header
- `jwt.decode()` verifies token signature with `SECRET_KEY`
- User ID extracted from `sub` claim (Better Auth standard)
- User loaded from database for use in endpoints
- Returns User object or raises 401

### 3. Protected Endpoints

```python
from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/")
async def get_todos(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get all todos for authenticated user."""
    statement = select(Todo).where(Todo.user_id == current_user.id)
    result = await session.exec(statement)
    return result.all()

@router.post("/")
async def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create new todo for authenticated user."""
    db_todo = Todo(
        **todo.dict(),
        user_id=current_user.id  # Always use authenticated user
    )
    session.add(db_todo)
    await session.commit()
    return db_todo
```

**Key Concepts:**
- Inject `current_user` via `Depends(get_current_user)`
- Always filter/assign data by `current_user.id`
- Automatic 401 response if token invalid
- No need to manually verify tokens in endpoints

### 4. Backend Environment Variables

Create `.env`:

```bash
# MUST match frontend secret
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host/db

# Environment
ENVIRONMENT=development
```

## Token Structure

Better Auth generates JWT tokens with this structure:

```json
{
  "sub": "user-id-123",           // User ID (required)
  "email": "user@example.com",     // User email (optional)
  "iat": 1234567890,               // Issued at timestamp
  "exp": 1234567890                // Expiration timestamp
}
```

**Key Claims:**
- `sub` - Subject (user ID) - **This is what you extract in backend**
- `email` - User's email address
- `iat` - Issued at (timestamp)
- `exp` - Expiration (timestamp)

## Security Best Practices

### 1. Environment Variable Security

```typescript
// Frontend - next.config.js
module.exports = {
  env: {
    BETTER_AUTH_SECRET: process.env.BETTER_AUTH_SECRET,
  },
}
```

**Never expose secrets in client-side code!**

### 2. Token Expiration

```typescript
// lib/auth.ts
export const auth = betterAuth({
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,     // Refresh after 24 hours
  },
})
```

### 3. HTTPS in Production

```python
# Backend - only accept HTTPS in production
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(
        HTTPSRedirectMiddleware
    )
```

### 4. CORS Configuration

```python
# Backend - only allow your frontend domain
origins = ["https://your-app.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Protecting Routes

### Frontend (Next.js Middleware)

Create `middleware.ts`:

```typescript
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  // Check for Better Auth session cookie
  const session = request.cookies.get("better-auth.session_token")
  
  // Redirect to login if not authenticated
  if (!session && !request.nextUrl.pathname.startsWith("/login")) {
    return NextResponse.redirect(new URL("/login", request.url))
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/todos/:path*",
    // Add protected routes here
  ],
}
```

### Backend (Dependency Injection)

```python
from fastapi import APIRouter, Depends

# Apply to all routes in router
router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    dependencies=[Depends(get_current_user)]  # All routes protected
)

# Or per-endpoint
@router.get("/", dependencies=[Depends(get_current_user)])
async def get_todos():
    pass
```

## Error Handling

### Frontend

```typescript
const handleSignIn = async () => {
  const result = await signIn.email({ email, password })
  
  if (result.error) {
    // Handle auth errors
    switch (result.error.status) {
      case 401:
        setError("Invalid email or password")
        break
      case 429:
        setError("Too many attempts. Please try again later")
        break
      default:
        setError("An error occurred. Please try again")
    }
  }
}
```

### Backend

```python
from fastapi import HTTPException

async def get_current_user(...):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing user ID"
            )
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )
```

## When to Query Context7

Use the `using-context7` skill to query for:

```
✅ "Better Auth installation and setup Next.js 16"
✅ "Better Auth JWT configuration options"
✅ "Better Auth React hooks usage patterns"
✅ "Better Auth session management"
✅ "python-jose JWT decode and verify"
✅ "FastAPI HTTPBearer authentication"
```

Don't query for:
```
❌ JWT basics (structure, claims, signatures)
❌ HTTP Authorization header format
❌ Basic authentication concepts
```

## Common Patterns

### 1. Sign Up Flow

```typescript
const handleSignUp = async () => {
  const result = await signUp.email({
    email,
    password,
    name,
  })
  
  if (result.error) {
    setError(result.error.message)
  } else {
    // Redirect to dashboard or auto-login
    router.push("/dashboard")
  }
}
```

### 2. Check Auth Status

```typescript
"use client"

import { useSession } from "@/lib/auth-client"
import { useRouter } from "next/navigation"
import { useEffect } from "react"

export function ProtectedPage() {
  const { data: session, isPending } = useSession()
  const router = useRouter()
  
  useEffect(() => {
    if (!isPending && !session) {
      router.push("/login")
    }
  }, [session, isPending, router])
  
  if (isPending) return <div>Loading...</div>
  if (!session) return null
  
  return <div>Protected content</div>
}
```

### 3. API Client Wrapper

```typescript
// lib/api-client.ts
import { authClient } from "./auth-client"

export async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
) {
  const session = authClient.useSession()
  
  if (!session?.session.token) {
    throw new Error("Not authenticated")
  }
  
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Authorization": `Bearer ${session.session.token}`,
        "Content-Type": "application/json",
        ...options.headers,
      },
    }
  )
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }
  
  return response.json()
}

// Usage
const todos = await apiRequest("/todos")
```

## Testing

### Frontend (with Auth Mock)

```typescript
import { render, screen } from "@testing-library/react"
import { useSession } from "@/lib/auth-client"

jest.mock("@/lib/auth-client")

test("shows login when not authenticated", () => {
  (useSession as jest.Mock).mockReturnValue({
    data: null,
    isPending: false,
  })
  
  render(<ProtectedComponent />)
  expect(screen.getByText("Please log in")).toBeInTheDocument()
})
```

### Backend (with Auth Mock)

```python
from fastapi.testclient import TestClient

def test_protected_endpoint():
    # Mock authentication
    app.dependency_overrides[get_current_user] = lambda: User(id="test-user")
    
    response = client.get("/api/todos")
    assert response.status_code == 200
```

## Related Skill Files

- `reference.md` - Quick reference for Better Auth patterns
- `examples.md` - Complete auth implementation examples

## Remember

- **Shared secret** - `BETTER_AUTH_SECRET` must match frontend and backend
- **User ID in sub** - Extract from `payload.get("sub")` in backend
- **Always filter by user_id** - Multi-tenant security is critical
- **Token in header** - `Authorization: Bearer <token>`
- **Session hooks** - Use `useSession()` for auth state
- **Dependency injection** - `Depends(get_current_user)` in FastAPI
- **Query Context7** - For Better Auth specifics, not JWT basics

This skill provides complete authentication coverage for Phase 2. Combine with `fastapi-async-patterns` for protected endpoints and `nextjs-16-app-router` for frontend auth flows.