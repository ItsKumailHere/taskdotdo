api-client.md
# API Client Patterns

## Server-Side Fetch
```ts
export async function apiFetch(path: string, token: string) {
  return fetch(`${API_URL}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  })
}

Client Components

❌ Never call FastAPI directly
✅ Call Server Components or Server Actions

Environment Variables

NEXT_PUBLIC_API_URL

BETTER_AUTH_SECRET (server only)


---

