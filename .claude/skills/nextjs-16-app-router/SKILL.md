---
name: nextjs-16-app-router
description: Enforces correct Next.js 16 App Router usage. Use when building pages, layouts, routing, data fetching, or deciding between Server vs Client Components in Next.js 16 / React 19.
---

# Next.js 16 App Router Skill

This Skill enforces **correct, modern, production-safe App Router patterns** for Next.js 16.

## Core Rules (Non-Negotiable)

1. **Server Components by default**
   - Every file in `app/` is a Server Component unless explicitly marked with `"use client"`.

2. **Client Components ONLY when**
   - Browser-only APIs are required (`window`, `localStorage`)
   - React client hooks are required (`useState`, `useEffect`)
   - Event handlers or interactive UI is needed

3. **Data Fetching Rules**
   - Prefer fetching data in:
     - Server Components
     - Route Handlers (`app/api/**/route.ts`)
     - Server Actions
   - Client-side fetching is allowed **only** for:
     - highly interactive
     - real-time
     - user-triggered updates  
     and must be deliberate (e.g., SWR, React Query).

4. **Routing is file-system driven**
   - No custom routers
   - No conditional route trees

5. **Auth boundaries are strict**
   - Tokens and secrets may only exist in:
     - Server Components
     - Middleware
     - Route Handlers
     - Server Actions
   - Client Components receive data, never credentials.

For detailed rules, see:
- [routing.md](routing.md)
- [data-fetching.md](data-fetching.md)
- [auth-boundaries.md](auth-boundaries.md)

---

## When to Query Context7

Use Context7 **only when version-specific behavior matters**, such as:
- App Router middleware behavior
- Route handler semantics
- React 19 Server Actions
- Caching defaults in Next.js 16+

Avoid querying Context7 for:
- basic routing
- React fundamentals
