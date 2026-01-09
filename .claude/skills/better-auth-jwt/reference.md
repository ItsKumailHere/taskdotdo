# Better Auth JWT Quick Reference

## Installation

```bash
# Frontend
npm install better-auth

# Backend
pip install python-jose[cryptography] passlib[bcrypt]
```

## Frontend Setup

### 1. Auth Configuration (`lib/auth.ts`)

```typescript
import { betterAuth } from "better-auth"
import { nextCookies } from "better-auth/next-js"

export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
  },
  secret: process.env.BETTER_AUTH_SECRET!,
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,      // Update daily
  },
  plugins: [nextCookies()],
})
```

### 2. API Route Handler (`app/api/auth/[...all]/route.ts`)

```typescript
import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

export const { GET, POST } = toNextJsHandler(auth)
```

### 3. Auth Client (`lib/auth-client.ts`)

```typescript
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000",
})

export const { useSession, signIn, signOut, signUp } = authClient
```

## React Hooks

### useSession

```typescript
const { data: session, isPending, error } = useSession()

// Session structure
session = {
  user: {
    id: string
    email: string
    name: string
  },
  session: {
    token: string
    expiresAt: Date
  }
}
```

### signIn

```typescript
// Email & Password
const result = await signIn.email({
  email: "user@example.com",
  password: "password123",
})

if (result.error) {
  console.error(result.error.message)
}
```

### signOut

```typescript
await signOut()
// Clears session and redirects to home
```

### signUp

```typescript
const result = await signUp.email({
  email: "user@example.com",
  password: "password123",
  name: "John Doe",
})
```

## Making Authenticated Requests

### Basic Pattern

```typescript
const { data: session } = useSession()

const response = await fetch(`${API_URL}/todos`, {
  headers: {
    "Authorization": `Bearer ${session.session.token}`,
    "Content-Type": "application/json",
  },
})
```

### With Error Handling

```typescript
async function fetchTodos() {
  if (!session?.session.token) {
    throw new Error("Not authenticated")
  }

  const response = await fetch(`${API_URL}/todos`, {
    headers: {
      "Authorization": `Bearer ${session.session.token}`,
      "Content-Type": "application/json",
    },
  })

  if (response.status === 401) {
    // Token expired or invalid
    await signOut()
    throw new Error("Session expired")
  }

  if (!response.ok) {
    throw new Error("Failed to fetch todos")
  }

  return response.json()
}
```

## Frontend Middleware (Route Protection)

```typescript
// middleware.ts
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  const session = request.cookies.get("better-auth.session_token")
  
  if (!session && !request.nextUrl.pathname.startsWith("/login")) {
    return NextResponse.redirect(new URL("/login", request.url))
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*", "/todos/:path*"],
}
```

## Backend Setup

### JWT Verification (`app/auth.py`)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import get_session
from app.models import User
import os

security = HTTPBearer()
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
            
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    user = result.first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user
```

### Protected Endpoints

```python
from fastapi import APIRouter, Depends
from app.auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/")
async def get_todos(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    statement = select(Todo).where(Todo.user_id == current_user.id)
    result = await session.exec(statement)
    return result.all()
```

### Apply Auth to All Routes in Router

```python
router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    dependencies=[Depends(get_current_user)]  # All routes protected
)
```

## Environment Variables

### Frontend (`.env.local`)

```bash
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Backend (`.env`)

```bash
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
```

**Critical:** Both must use the SAME secret key!

## JWT Token Structure

```json
{
  "sub": "user-id-123",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234567890
}
```

**Extract user_id from `sub` claim in backend**

## Common UI Patterns

### Login Form

```typescript
"use client"

import { useState } from "react"
import { signIn } from "@/lib/auth-client"

export function LoginForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const result = await signIn.email({ email, password })
    
    if (result.error) {
      setError(result.error.message)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button type="submit">Sign In</button>
      {error && <p>{error}</p>}
    </form>
  )
}
```

### Auth Status Display

```typescript
"use client"

import { useSession, signOut } from "@/lib/auth-client"

export function AuthStatus() {
  const { data: session, isPending } = useSession()

  if (isPending) return <div>Loading...</div>

  if (!session) {
    return <a href="/login">Sign In</a>
  }

  return (
    <div>
      <span>Welcome, {session.user.email}</span>
      <button onClick={() => signOut()}>Sign Out</button>
    </div>
  )
}
```

### Protected Component

```typescript
"use client"

import { useSession } from "@/lib/auth-client"
import { useEffect } from "react"
import { useRouter } from "next/navigation"

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

## API Client Wrapper

```typescript
// lib/api.ts
import { authClient } from "./auth-client"

export async function api<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
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
    if (response.status === 401) {
      await authClient.signOut()
    }
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}

// Usage
const todos = await api<Todo[]>("/todos")
const newTodo = await api<Todo>("/todos", {
  method: "POST",
  body: JSON.stringify({ title: "New todo" }),
})
```

## Error Handling

### Frontend Errors

```typescript
const result = await signIn.email({ email, password })

if (result.error) {
  switch (result.error.status) {
    case 401:
      setError("Invalid credentials")
      break
    case 429:
      setError("Too many attempts")
      break
    default:
      setError("An error occurred")
  }
}
```

### Backend Errors

```python
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token expired")
except jwt.JWTError as e:
    raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
```

## Testing

### Frontend (Mock useSession)

```typescript
import { useSession } from "@/lib/auth-client"

jest.mock("@/lib/auth-client")

test("shows content when authenticated", () => {
  (useSession as jest.Mock).mockReturnValue({
    data: {
      user: { id: "1", email: "test@example.com" },
      session: { token: "test-token" }
    },
    isPending: false,
  })
  
  render(<ProtectedComponent />)
  expect(screen.getByText("Protected content")).toBeInTheDocument()
})
```

### Backend (Override Dependency)

```python
from fastapi.testclient import TestClient

def test_protected_endpoint():
    app.dependency_overrides[get_current_user] = lambda: User(
        id="test-user",
        email="test@example.com"
    )
    
    response = client.get("/api/todos")
    assert response.status_code == 200
```

## Configuration Options

### Session Configuration

```typescript
session: {
  expiresIn: 60 * 60 * 24 * 7,  // 7 days (seconds)
  updateAge: 60 * 60 * 24,       // Update every 24 hours
  cookieName: "better-auth.session_token",
}
```

### JWT Algorithm

```python
# Backend - must match Better Auth
ALGORITHM = "HS256"  # Default for Better Auth
```

## Security Checklist

- ✅ Use strong secret (min 32 characters)
- ✅ Same secret in frontend and backend
- ✅ Never commit secrets to git
- ✅ Use HTTPS in production
- ✅ Set appropriate token expiration
- ✅ Validate tokens on every request
- ✅ Always filter data by user_id
- ✅ Configure CORS properly
- ✅ Handle token expiration gracefully

## Quick Command Reference

| Task | Code |
|------|------|
| **Get session** | `const { data: session } = useSession()` |
| **Sign in** | `await signIn.email({ email, password })` |
| **Sign out** | `await signOut()` |
| **Get token** | `session.session.token` |
| **Protected request** | `{ headers: { "Authorization": "Bearer ${token}" } }` |
| **Backend verify** | `Depends(get_current_user)` |
| **Extract user_id** | `payload.get("sub")` |

---

This reference covers all Better Auth JWT patterns needed for Phase 2!