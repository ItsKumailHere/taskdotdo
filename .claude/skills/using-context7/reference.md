# Context7 Query Reference

## MCP Tool Syntax

Context7 is accessed via the `context7_query` MCP tool:

```typescript
context7_query({
  query: "Your specific documentation query here"
})
```

## Query Pattern Templates

### Next.js 16 Queries

```
Installation & Setup:
"Next.js 16 App Router project initialization"
"Next.js 16 TypeScript configuration"

Routing & Pages:
"Next.js 16 App Router file-based routing conventions"
"Next.js 16 dynamic routes with [id] syntax"
"Next.js 16 route groups and layouts"
"Next.js 16 parallel routes and intercepting routes"

Components:
"Next.js 16 Server Components vs Client Components differences"
"Next.js 16 when to use 'use client' directive"
"Next.js 16 async Server Components patterns"

Data Fetching:
"Next.js 16 fetch API with cache options"
"Next.js 16 server-side data fetching in components"
"Next.js 16 loading and error UI patterns"
"Next.js 16 revalidation strategies"

API Routes:
"Next.js 16 App Router route handlers"
"Next.js 16 route handler request and response types"
"Next.js 16 middleware for API routes"

Middleware:
"Next.js 16 middleware.ts configuration"
"Next.js 16 middleware for authentication"
"Next.js 16 middleware matcher patterns"

Deployment:
"Next.js 16 Vercel deployment configuration"
"Next.js 16 environment variables"
```

### FastAPI Queries

```
Setup & Configuration:
"FastAPI async application initialization"
"FastAPI CORS middleware configuration"
"FastAPI dependency injection system"

Endpoints:
"FastAPI async endpoint patterns"
"FastAPI request body validation with Pydantic v2"
"FastAPI response models and status codes"
"FastAPI path and query parameters"

Database Integration:
"FastAPI SQLModel async session management"
"FastAPI database dependency injection"
"FastAPI connection pooling patterns"

Authentication:
"FastAPI JWT authentication dependency"
"FastAPI OAuth2 password bearer"
"FastAPI security utilities"

Error Handling:
"FastAPI exception handlers"
"FastAPI HTTPException usage"
"FastAPI custom error responses"

Testing:
"FastAPI TestClient usage"
"FastAPI async test patterns"
```

### SQLModel Queries

```
Setup:
"SQLModel installation with async support"
"SQLModel engine configuration for PostgreSQL"

Models:
"SQLModel table models with Field definitions"
"SQLModel optional fields and defaults"
"SQLModel relationship patterns with Relationship"
"SQLModel back_populates configuration"

Queries:
"SQLModel async select statements"
"SQLModel where clause filtering"
"SQLModel relationship loading with selectinload"
"SQLModel join queries"

Sessions:
"SQLModel async session management"
"SQLModel session context managers"
"SQLModel commit and rollback patterns"

Migrations:
"SQLModel with Alembic setup"
"SQLModel create_all for initial schema"
```

### Better Auth Queries

```
Setup:
"Better Auth installation for Next.js 16"
"Better Auth configuration file structure"
"Better Auth environment variables"

Authentication:
"Better Auth JWT token generation"
"Better Auth session management"
"Better Auth email/password provider setup"

Frontend:
"Better Auth React hooks for auth state"
"Better Auth signIn and signOut functions"
"Better Auth useSession hook"
"Better Auth protecting routes in Next.js 16"

Backend Integration:
"Better Auth JWT verification in backend"
"Better Auth token structure and claims"
"Better Auth BETTER_AUTH_SECRET usage"

API Routes:
"Better Auth API route handlers in Next.js 16"
"Better Auth callback URLs configuration"
```

### Neon PostgreSQL Queries

```
Setup:
"Neon PostgreSQL connection string format"
"Neon serverless driver configuration"

Integration:
"Neon with SQLModel async engine"
"Neon connection pooling settings"
"Neon serverless-specific optimizations"

Deployment:
"Neon database URL in Vercel environment"
"Neon branching for development"
```

## Query Refinement Patterns

### From Broad to Specific

```
Round 1: "FastAPI database integration"
         ↓ (Too broad, refine)
Round 2: "FastAPI SQLModel async session"
         ↓ (Better, but need specific pattern)
Round 3: "FastAPI SQLModel async session dependency injection pattern"
         ✓ (Specific enough)
```

### Adding Context

```
Base:     "Next.js authentication"
+ Tech:   "Next.js 16 authentication"
+ Method: "Next.js 16 JWT authentication"
+ Tool:   "Next.js 16 JWT authentication with Better Auth"
+ Goal:   "Next.js 16 middleware for JWT authentication with Better Auth"
         ✓ (Complete context)
```

## Multi-Part Implementation Queries

For complex features, break into sequential queries:

### Example: Full Auth Flow

```
1. Frontend Setup:
   "Better Auth installation and basic configuration Next.js 16"

2. Auth Routes:
   "Better Auth API route handlers in Next.js 16 App Router"

3. Backend Verification:
   "FastAPI JWT verification for Better Auth tokens"

4. Protected Endpoints:
   "FastAPI protected routes with JWT dependency injection"

5. Frontend Auth State:
   "Better Auth useSession hook and auth state management"

6. Middleware Protection:
   "Next.js 16 middleware for protecting routes with Better Auth"
```

## Common Query Mistakes

### ❌ Too Vague
```
"authentication"
"database queries"  
"error handling"
```

### ✓ Just Right
```
"Better Auth JWT setup for Next.js 16 App Router"
"SQLModel async select queries with relationship loading"
"FastAPI HTTPException custom error responses"
```

### ❌ Over-Specific (Unlikely to Match Docs)
```
"Better Auth JWT verification in FastAPI for todo app with user_id filtering"
"SQLModel query to get all todos for user 123 ordered by created_at"
```

### ✓ Framework-Focused (Matches Docs)
```
"Better Auth JWT verification in Python backend"
"SQLModel filtering queries with where clause"
```

## Performance Tips

1. **Cache Query Results**: Store information from Context7 responses in your working memory for the session

2. **One Query Per Feature**: Don't re-query for variations of the same topic

3. **Query Before Implementation**: Get docs first, then implement, rather than implementing → hitting error → querying

4. **Combine Related Topics**: 
   ```
   ✓ "FastAPI async endpoints with SQLModel and dependency injection"
   ✗ Three separate queries for async, SQLModel, and DI
   ```

## Query Priority Matrix

```
┌─────────────┬──────────────────────┬──────────────────────┐
│  Priority   │   When to Query      │      Example         │
├─────────────┼──────────────────────┼──────────────────────┤
│ 🔴 Critical │ Before implementing  │ Better Auth setup    │
│             │ unfamiliar framework │ Next.js 16 patterns  │
├─────────────┼──────────────────────┼──────────────────────┤
│ 🟡 Optional │ If implementation    │ Optimizing queries   │
│             │ hits unexpected issue│ Advanced patterns    │
├─────────────┼──────────────────────┼──────────────────────┤
│ 🟢 Skip     │ Basic concepts       │ HTTP methods         │
│             │ Well-known patterns  │ Python syntax        │
└─────────────┴──────────────────────┴──────────────────────┘
```

---

Use these patterns as templates, not rigid scripts. Adapt queries to your specific needs while maintaining specificity about framework, version, and context.