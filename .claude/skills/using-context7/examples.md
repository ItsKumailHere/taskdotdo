# Real-World Context7 Query Examples for Phase 2

## Scenario-Based Query Examples

### Scenario 1: Setting Up Better Auth

**Task**: Install and configure Better Auth for JWT authentication

**Query Sequence**:
```
1. Initial Setup:
   "Better Auth installation for Next.js 16 App Router"
   
   Response: Installation steps, package names
   Action: npm install, create auth.ts config

2. Configuration:
   "Better Auth JWT configuration with environment variables"
   
   Response: BETTER_AUTH_SECRET, JWT options, session config
   Action: Set up .env.local, configure auth.ts

3. API Routes:
   "Better Auth API route handler in Next.js 16 /api/auth/[...all]"
   
   Response: Route handler structure, export patterns
   Action: Create app/api/auth/[...all]/route.ts
```

**Outcome**: Better Auth fully configured and running

---

### Scenario 2: Building FastAPI CRUD Endpoints

**Task**: Create async CRUD endpoints with SQLModel

**Query Sequence**:
```
1. Database Setup:
   "FastAPI SQLModel async engine and session configuration"
   
   Response: Engine creation, AsyncSession setup
   Action: Create database.py with engine and get_session

2. Dependency Injection:
   "FastAPI async dependency injection with database session"
   
   Response: Depends() pattern, session lifecycle
   Action: Create get_db() dependency

3. CRUD Patterns:
   "FastAPI async CRUD endpoints with SQLModel select and insert"
   
   Response: Route patterns, session.execute(), session.add()
   Action: Create todos.py router with CRUD operations
```

**Outcome**: Working API endpoints with proper async/await

---

### Scenario 3: JWT Verification in FastAPI

**Task**: Verify Better Auth JWT tokens in backend

**Query Sequence**:
```
1. JWT Basics:
   "FastAPI JWT token verification with python-jose"
   
   Response: jwt.decode(), algorithms, secret keys
   Action: Install python-jose, create auth utilities

2. Dependency Pattern:
   "FastAPI JWT authentication dependency for protected routes"
   
   Response: OAuth2PasswordBearer, verify_token dependency
   Action: Create get_current_user() dependency

3. User Extraction:
   "Better Auth JWT token claims structure and user_id extraction"
   
   Response: Token payload format, claims mapping
   Action: Extract user_id from token, use in endpoints
```

**Outcome**: Protected endpoints filtering by authenticated user

---

### Scenario 4: SQLModel Relationships

**Task**: Create User and Todo models with relationships

**Query Sequence**:
```
1. Model Structure:
   "SQLModel table models with Field and relationship definitions"
   
   Response: Field syntax, primary keys, foreign keys
   Action: Define User and Todo models

2. Relationships:
   "SQLModel Relationship back_populates pattern for one-to-many"
   
   Response: Relationship field, List typing, back_populates
   Action: Add todos relationship to User, user to Todo

3. Querying:
   "SQLModel select with relationship loading using selectinload"
   
   Response: selectinload() usage, options() method
   Action: Optimize queries to load user.todos efficiently
```

**Outcome**: Proper User-Todo relationships with efficient loading

---

### Scenario 5: Next.js 16 Server vs Client Components

**Task**: Build todo list with proper component types

**Query Sequence**:
```
1. Component Types:
   "Next.js 16 Server Components vs Client Components when to use"
   
   Response: Default server, 'use client' directive, trade-offs
   Action: Decide which components need 'use client'

2. Data Fetching:
   "Next.js 16 Server Component async data fetching with fetch"
   
   Response: async component syntax, fetch with cache options
   Action: Create async TodoList server component

3. Interactivity:
   "Next.js 16 Client Component for forms and user interactions"
   
   Response: 'use client' placement, useState, event handlers
   Action: Create AddTodoForm client component
```

**Outcome**: Optimized component architecture (server where possible)

---

### Scenario 6: Frontend API Integration

**Task**: Connect Next.js frontend to FastAPI backend

**Query Sequence**:
```
1. API Client:
   "Next.js 16 fetch API with Authorization header and JWT token"
   
   Response: fetch syntax, headers, Bearer token format
   Action: Create API client utility with auth headers

2. Error Handling:
   "Next.js 16 error handling for failed fetch requests"
   
   Response: try-catch patterns, error boundaries, error.tsx
   Action: Add error handling and user feedback

3. Revalidation:
   "Next.js 16 revalidatePath after mutations"
   
   Response: revalidatePath() usage, when to call it
   Action: Refresh UI after create/update/delete operations
```

**Outcome**: Seamless frontend-backend communication with auth

---

### Scenario 7: Deployment to Vercel

**Task**: Deploy full-stack app to Vercel

**Query Sequence**:
```
1. Frontend Deployment:
   "Next.js 16 Vercel deployment configuration"
   
   Response: vercel.json, build settings, environment variables
   Action: Configure vercel.json for frontend

2. Backend Deployment:
   "FastAPI deployment on Vercel as serverless function"
   
   Response: vercel.json rewrites, api/ folder structure
   Action: Configure backend as Vercel function

3. Environment Variables:
   "Vercel environment variables for DATABASE_URL and secrets"
   
   Response: Vercel dashboard settings, .env.production
   Action: Set DATABASE_URL, BETTER_AUTH_SECRET in Vercel
```

**Outcome**: Full-stack app deployed and running on Vercel

---

## Anti-Patterns: Queries That DON'T Need Context7

### ❌ Don't Query For These:

```
"Python async await syntax"
→ You already know async/await

"HTTP POST request format"
→ Standard HTTP knowledge

"React useState hook"
→ Fundamental React hook

"SQL SELECT statement"
→ Basic SQL syntax

"JSON serialization in Python"
→ Standard library feature

"CSS Tailwind classes"
→ Standard Tailwind utilities

"Git commit commands"
→ Basic Git usage

"Environment variables in Node.js"
→ process.env is standard
```

### ✅ Query For These Instead:

```
"Better Auth token refresh flow"
→ Framework-specific implementation

"Next.js 16 middleware execution order"
→ Version-specific behavior

"SQLModel async session best practices with FastAPI"
→ Integration pattern between frameworks

"Neon PostgreSQL connection string format for SQLModel"
→ Provider-specific configuration

"Vercel serverless function timeout limits"
→ Platform-specific constraint

"Better Auth React hooks TypeScript types"
→ Framework-specific types
```

---

## Query Timing: Before vs During vs After

### Before Implementation (Recommended)
```
Query: "FastAPI async background tasks"
Implement: Background task for sending emails
Result: ✓ Done right the first time
```

### During Implementation (Acceptable)
```
Start implementing → Hit uncertainty → Query → Continue
Result: ✓ Minimal backtracking
```

### After Implementation (Inefficient)
```
Implement based on guesses → Bugs appear → Query → Rewrite
Result: ✗ Wasted time, potential tech debt
```

---

## Progressive Query Example: Building Auth System

### Initial Query (Broad)
```
Query: "Better Auth Next.js 16 setup"
Response: Basic installation and config
Action: Install packages, create basic config
```

### Follow-Up Query (Specific)
```
Query: "Better Auth JWT token generation with custom claims"
Response: Token customization in auth.ts
Action: Add user_id and email to JWT payload
```

### Refinement Query (Edge Case)
```
Query: "Better Auth token refresh on expiration"
Response: Refresh token flow, session extension
Action: Implement automatic token refresh
```

### Integration Query (Cross-Stack)
```
Query: "FastAPI verify Better Auth JWT signature"
Response: Shared secret verification, python-jose
Action: Create verify_token() in backend
```

**Result**: Complete, production-ready auth system built incrementally with targeted queries

---

## Key Takeaways

1. **Query before implementing** unfamiliar framework features
2. **Be specific** about framework, version, and context
3. **Break complex features** into sequential queries
4. **Don't re-query** for information already obtained
5. **Skip queries** for basic programming concepts
6. **Combine related topics** in single queries when possible
7. **Use query results** as implementation guide, not just reference

These examples represent actual Phase 2 tasks. Use them as templates for your own Context7 queries during development.