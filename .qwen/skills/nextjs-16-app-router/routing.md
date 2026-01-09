# Routing Rules — Next.js 16

## File Types
- `page.tsx` → Route entry
- `layout.tsx` → Persistent UI
- `loading.tsx` → Suspense boundary
- `error.tsx` → Error boundary
- `not-found.tsx` → 404 handling
- `route.ts` → API endpoints (App Router)

## Route Handlers (`route.ts`)
- Used for backend-style APIs
- Can read headers, cookies, tokens
- Can call databases or FastAPI
- Preferred over legacy API routes

## Layout Rules
- Layouts are Server Components
- Fetch shared user data in layouts when possible
- Auth-protected sections should be wrapped via layout

## Middleware
Use middleware **only** for:
- auth gating
- redirects
- URL rewriting

Middleware must be:
- lightweight
- side-effect free