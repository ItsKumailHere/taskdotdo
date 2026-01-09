# Better Auth JWT Real-World Examples for Phase 2

## Example 1: Complete Authentication Setup

### Frontend Structure
```
frontend/
├── lib/
│   ├── auth.ts           # Better Auth configuration
│   ├── auth-client.ts    # React hooks export
│   └── api.ts            # Authenticated API client
├── app/
│   ├── api/
│   │   └── auth/
│   │       └── [...all]/route.ts  # Better Auth handler
│   ├── login/
│   │   └── page.tsx      # Login page
│   ├── signup/
│   │   └── page.tsx      # Signup page
│   └── dashboard/
│       └── page.tsx      # Protected dashboard
├── components/
│   ├── LoginForm.tsx
│   ├── SignupForm.tsx
│   └── AuthStatus.tsx
├── middleware.ts          # Route protection
└── .env.local
```

### lib/auth.ts (Configuration)

```typescript
import { betterAuth } from "better-auth"
import { nextCookies } from "better-auth/next-js"

export const auth = betterAuth({
  // Email & Password authentication
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    requireEmailVerification: false, // Set true in production
  },
  
  // JWT configuration
  secret: process.env.BETTER_AUTH_SECRET!,
  
  // Session settings
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
    updateAge: 60 * 60 * 24,      // Refresh session every 24 hours
    cookieName: "better-auth.session_token",
  },
  
  // Next.js integration
  plugins: [
    nextCookies({
      sameSite: "lax",  // CSRF protection
      secure: process.env.NODE_ENV === "production", // HTTPS only in production
    })
  ],
  
  // Base URL
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
})
```

### lib/auth-client.ts (React Hooks)

```typescript
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
})

// Export individual hooks for convenience
export const {
  useSession,
  signIn,
  signOut,
  signUp,
} = authClient

// Type-safe session
export type Session = Awaited<ReturnType<typeof useSession>>["data"]
```

### app/api/auth/[...all]/route.ts

```typescript
import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

// Export GET and POST handlers
export const { GET, POST } = toNextJsHandler(auth)

// This creates these endpoints automatically:
// POST /api/auth/sign-in
// POST /api/auth/sign-up
// POST /api/auth/sign-out
// GET  /api/auth/session
// And more...
```

---

## Example 2: Login & Signup Forms

### components/LoginForm.tsx

```typescript
"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { signIn } from "@/lib/auth-client"

export function LoginForm() {
  const router = useRouter()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    try {
      const result = await signIn.email({
        email,
        password,
      })

      if (result.error) {
        setError(result.error.message)
      } else {
        // Redirect to dashboard on success
        router.push("/dashboard")
      }
    } catch (err) {
      setError("An unexpected error occurred")
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border p-2"
          disabled={loading}
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
          className="mt-1 block w-full rounded-md border p-2"
          disabled={loading}
        />
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Signing in..." : "Sign In"}
      </button>

      <p className="text-center text-sm">
        Don't have an account?{" "}
        <a href="/signup" className="text-blue-600 hover:underline">
          Sign up
        </a>
      </p>
    </form>
  )
}
```

### components/SignupForm.tsx

```typescript
"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { signUp } from "@/lib/auth-client"

export function SignupForm() {
  const router = useRouter()
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    // Validate passwords match
    if (password !== confirmPassword) {
      setError("Passwords do not match")
      return
    }

    // Validate password strength
    if (password.length < 8) {
      setError("Password must be at least 8 characters")
      return
    }

    setLoading(true)

    try {
      const result = await signUp.email({
        email,
        password,
        name,
      })

      if (result.error) {
        setError(result.error.message)
      } else {
        // Redirect to dashboard on success
        router.push("/dashboard")
      }
    } catch (err) {
      setError("An unexpected error occurred")
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
      <div>
        <label htmlFor="name" className="block text-sm font-medium">
          Name
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border p-2"
          disabled={loading}
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border p-2"
          disabled={loading}
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
          className="mt-1 block w-full rounded-md border p-2"
          disabled={loading}
        />
      </div>

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium">
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          minLength={8}
          className="mt-1 block w-full rounded-md border p-2"
          disabled={loading}
        />
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Creating account..." : "Sign Up"}
      </button>

      <p className="text-center text-sm">
        Already have an account?{" "}
        <a href="/login" className="text-blue-600 hover:underline">
          Sign in
        </a>
      </p>
    </form>
  )
}
```

---

## Example 3: Auth Status & Navigation

### components/AuthStatus.tsx

```typescript
"use client"

import { useSession, signOut } from "@/lib/auth-client"
import { useRouter } from "next/navigation"

export function AuthStatus() {
  const { data: session, isPending } = useSession()
  const router = useRouter()

  const handleSignOut = async () => {
    await signOut()
    router.push("/")
  }

  if (isPending) {
    return (
      <div className="animate-pulse">
        <div className="h-8 w-24 bg-gray-200 rounded"></div>
      </div>
    )
  }

  if (!session) {
    return (
      <div className="flex gap-2">
        <a
          href="/login"
          className="px-4 py-2 text-blue-600 hover:text-blue-700"
        >
          Sign In
        </a>
        <a
          href="/signup"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Sign Up
        </a>
      </div>
    )
  }

  return (
    <div className="flex items-center gap-4">
      <span className="text-sm">
        Welcome, {session.user.name || session.user.email}
      </span>
      <button
        onClick={handleSignOut}
        className="px-4 py-2 text-sm text-red-600 hover:text-red-700"
      >
        Sign Out
      </button>
    </div>
  )
}
```

---

## Example 4: Protected Pages

### app/dashboard/page.tsx

```typescript
"use client"

import { useSession } from "@/lib/auth-client"
import { useRouter } from "next/navigation"
import { useEffect } from "react"

export default function DashboardPage() {
  const { data: session, isPending } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/login")
    }
  }, [session, isPending, router])

  if (isPending) {
    return <div>Loading...</div>
  }

  if (!session) {
    return null // Redirecting...
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user.email}!</p>
      {/* Protected content here */}
    </div>
  )
}
```

### middleware.ts (Route Protection)

```typescript
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  // Check for Better Auth session cookie
  const sessionToken = request.cookies.get("better-auth.session_token")
  
  const isAuthPage = request.nextUrl.pathname.startsWith("/login") ||
                     request.nextUrl.pathname.startsWith("/signup")
  
  const isProtectedPage = request.nextUrl.pathname.startsWith("/dashboard") ||
                          request.nextUrl.pathname.startsWith("/todos")

  // Redirect authenticated users away from auth pages
  if (sessionToken && isAuthPage) {
    return NextResponse.redirect(new URL("/dashboard", request.url))
  }

  // Redirect unauthenticated users to login
  if (!sessionToken && isProtectedPage) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/todos/:path*",
    "/login",
    "/signup",
  ],
}
```

---

## Example 5: Authenticated API Client

### lib/api.ts

```typescript
import { authClient } from "./auth-client"

class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = "APIError"
  }
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Get current session
  const sessionData = authClient.useSession()
  
  if (!sessionData?.data?.session?.token) {
    throw new APIError(401, "Not authenticated")
  }

  const token = sessionData.data.session.token

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
        ...options.headers,
      },
    }
  )

  if (response.status === 401) {
    // Token expired or invalid - sign out user
    await authClient.signOut()
    throw new APIError(401, "Session expired. Please sign in again.")
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }))
    throw new APIError(response.status, error.detail || "Request failed")
  }

  return response.json()
}

// Convenience methods
export const api = {
  get: <T>(endpoint: string) =>
    apiRequest<T>(endpoint, { method: "GET" }),

  post: <T>(endpoint: string, data: unknown) =>
    apiRequest<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  patch: <T>(endpoint: string, data: unknown) =>
    apiRequest<T>(endpoint, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  delete: <T>(endpoint: string) =>
    apiRequest<T>(endpoint, { method: "DELETE" }),
}

// Usage examples:
// const todos = await api.get<Todo[]>("/todos")
// const newTodo = await api.post<Todo>("/todos", { title: "New todo" })
// const updated = await api.patch<Todo>("/todos/123", { completed: true })
// await api.delete("/todos/123")
```

### Using the API Client in Components

```typescript
"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"

interface Todo {
  id: string
  title: string
  completed: boolean
}

export function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function fetchTodos() {
      try {
        const data = await api.get<Todo[]>("/todos")
        setTodos(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch todos")
      } finally {
        setLoading(false)
      }
    }

    fetchTodos()
  }, [])

  const handleToggle = async (id: string, completed: boolean) => {
    try {
      await api.patch(`/todos/${id}`, { completed: !completed })
      setTodos(todos.map(t => 
        t.id === id ? { ...t, completed: !completed } : t
      ))
    } catch (err) {
      setError("Failed to update todo")
    }
  }

  if (loading) return <div>Loading todos...</div>
  if (error) return <div className="text-red-600">{error}</div>

  return (
    <div>
      {todos.map(todo => (
        <div key={todo.id} className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => handleToggle(todo.id, todo.completed)}
          />
          <span className={todo.completed ? "line-through" : ""}>
            {todo.title}
          </span>
        </div>
      ))}
    </div>
  )
}
```

---

## Example 6: Backend JWT Verification

### Complete Backend Auth Setup

```python
# app/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import get_session
from app.models import User
import os
from datetime import datetime, timezone

# Security scheme for Swagger docs
security = HTTPBearer()

# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable must be set")

ALGORITHM = "HS256"

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Verify Better Auth JWT token and return current user.
    
    Token format from Better Auth:
    {
        "sub": "user-id-123",
        "email": "user@example.com",
        "iat": 1234567890,
        "exp": 1234567890
    }
    
    Raises:
        HTTPException: 401 if token invalid or user not found
    """
    token = credentials.credentials
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode and verify JWT token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        # Extract user ID from 'sub' claim
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError as e:
        print(f"JWT verification failed: {e}")
        raise credentials_exception
    
    # Fetch user from database
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    user = result.first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

# Optional: Dependency for optional authentication
async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User | None:
    """Same as get_current_user but returns None instead of raising exception."""
    try:
        return await get_current_user(credentials, session)
    except HTTPException:
        return None
```

---

## Example 7: Complete Phase 2 Auth Flow

### User Registration → Login → API Call

**Step 1: User Signs Up (Frontend)**
```typescript
// User fills out signup form
const result = await signUp.email({
  email: "user@example.com",
  password: "SecurePass123",
  name: "John Doe",
})

// Better Auth:
// 1. Creates user in its internal database
// 2. Generates JWT token with user_id in 'sub' claim
// 3. Sets session cookie
// 4. Returns session data
```

**Step 2: User Creates Todo (Frontend)**
```typescript
const { data: session } = useSession()

// Send request with JWT token
const response = await fetch(`${API_URL}/todos`, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${session.session.token}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ title: "My first todo" }),
})
```

**Step 3: Backend Verifies & Processes (Backend)**
```python
@router.post("/todos", response_model=TodoPublic)
async def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),  # Token verified here
    session: AsyncSession = Depends(get_session)
):
    # current_user is already authenticated User object
    db_todo = Todo(
        id=str(uuid4()),
        **todo.dict(),
        user_id=current_user.id  # Secure user isolation
    )
    
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    
    return db_todo
```

---

## Key Takeaways

1. **Shared Secret**: `BETTER_AUTH_SECRET` must be identical in frontend and backend
2. **Token Location**: Better Auth stores token in `session.session.token`
3. **Header Format**: Always `Authorization: Bearer <token>`
4. **User ID Extraction**: Backend extracts from `payload.get("sub")`
5. **User Isolation**: Always filter/assign data by `current_user.id`
6. **Error Handling**: Handle 401 responses by signing out user
7. **Route Protection**: Use middleware on frontend, dependencies on backend
8. **Token Expiration**: Configure appropriate expiration times
9. **HTTPS**: Always use HTTPS in production
10. **Testing**: Mock `useSession()` in frontend, override `get_current_user` in backend

These examples cover the complete authentication flow for Phase 2!