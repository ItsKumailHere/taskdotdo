# Data Fetching Rules

## Preferred Locations
✅ Server Components  
✅ Route Handlers (`app/api/**/route.ts`)  
✅ Server Actions  

## Client Components
Client-side fetching is allowed **only** when:
- data is interaction-driven
- real-time updates are required
- optimistic UI patterns are used

Examples:
- SWR
- React Query
- polling / subscriptions

Client Components must **never**:
- access secrets
- read auth tokens directly

## Default Fetch Pattern (Server)
```ts
const res = await fetch(`${API_URL}/todos`, {
  headers: { Authorization: `Bearer ${token}` },
  cache: "no-store"
})
