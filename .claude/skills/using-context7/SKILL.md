---
name: using-context7
description: Expert at finding and using official documentation via Context7 MCP for Next.js 16, React 19, FastAPI, Better Auth, and SQLModel. Teaches WHEN to query (framework specifics, not basics) and HOW to query effectively (specific vs broad).
---

# Using Context7 MCP - Master Documentation Skill

You are an expert at leveraging Context7 MCP to access current, official documentation for modern web frameworks. This skill teaches you **when** to query Context7 and **how** to query it effectively.

## Core Philosophy

**Context7 is for CURRENT, SPECIFIC framework knowledge - not basic concepts.**

### ✅ DO Query Context7 For:
- **Version-specific patterns** (Next.js 16 App Router vs Pages Router)
- **New APIs** released after your training cutoff (Jan 2025)
- **Configuration specifics** (Better Auth JWT setup, Neon connection strings)
- **Breaking changes** in recent versions
- **Official best practices** that may have evolved
- **Edge cases** in async patterns, authentication flows
- **Deployment configurations** (Vercel, serverless environments)

### ❌ DON'T Query Context7 For:
- Basic JavaScript/Python syntax
- General programming concepts (loops, conditionals, functions)
- Well-established patterns you know (REST principles, SQL basics)
- Obvious tasks you can complete without docs
- Information already in current conversation context

## When to Query: Decision Tree

```
Need to implement something?
    ↓
Do I know the current API/pattern confidently?
    ↓ Yes → Implement directly
    ↓ No
    ↓
Is this framework-specific? (Next.js 16, Better Auth, etc.)
    ↓ Yes → QUERY CONTEXT7
    ↓ No
    ↓
Is this a basic concept? (for loops, HTTP methods, etc.)
    ↓ Yes → Use existing knowledge
    ↓ No → Consider querying if it's specialized
```

## How to Query Effectively

### 1. Be Specific About Framework + Version
```
❌ Bad:  "authentication setup"
✅ Good: "Better Auth JWT configuration for Next.js 16 App Router"

❌ Bad:  "database queries"
✅ Good: "SQLModel async session management with Neon PostgreSQL"

❌ Bad:  "API endpoints"
✅ Good: "FastAPI async dependency injection patterns"
```

### 2. Include Context About Your Task
```
❌ Bad:  "middleware in Next.js"
✅ Good: "Next.js 16 middleware for JWT authentication with Better Auth"

❌ Bad:  "error handling"
✅ Good: "FastAPI exception handling with custom error responses"
```

### 3. Query Once Per Implementation Phase
Don't repeatedly query for the same information. Example workflow:

```
Phase 1: Setup
- Query: "Better Auth installation and initial setup Next.js 16"
- Implement auth configuration

Phase 2: Backend Integration  
- Query: "FastAPI JWT verification for Better Auth tokens"
- Implement verification endpoint

Phase 3: Frontend Flow
- Query: "Better Auth React hooks for authentication state"
- Implement login/logout UI
```

### 4. Progressive Specificity
Start specific, get more specific if needed:

```
Round 1: "FastAPI async SQLModel CRUD operations"
         → Implement basic CRUD

Round 2: "FastAPI SQLModel relationship loading with selectinload"
         → Optimize queries with relationships

Round 3: "FastAPI SQLModel pagination patterns"
         → Add pagination
```

## Framework-Specific Query Patterns

### Next.js 16 App Router
```
Topics to query:
- "Next.js 16 Server Components vs Client Components when to use"
- "Next.js 16 App Router data fetching with fetch cache"
- "Next.js 16 route handlers for API endpoints"
- "Next.js 16 middleware authentication patterns"
- "Next.js 16 server actions vs API routes"

NOT needed:
- Basic React hooks (useState, useEffect) - you know these
- CSS/Tailwind classes - standard knowledge
- Basic routing concepts - App Router structure is intuitive
```

### FastAPI + SQLModel
```
Topics to query:
- "FastAPI async endpoint patterns with SQLModel"
- "SQLModel async session management best practices"
- "FastAPI dependency injection with database sessions"
- "FastAPI Pydantic v2 response models"
- "SQLModel relationship patterns with back_populates"

NOT needed:
- Basic Python async/await - standard knowledge
- HTTP status codes - well-known
- JSON serialization basics - standard
```

### Better Auth + JWT
```
Topics to query:
- "Better Auth installation and configuration Next.js 16"
- "Better Auth JWT token generation and verification"
- "Better Auth React hooks usage patterns"
- "Better Auth session management"
- "Better Auth environment variables configuration"

NOT needed:
- General JWT concepts - you understand JWTs
- Cookie vs token storage - basic auth concepts
```

### Neon PostgreSQL + SQLModel
```
Topics to query:
- "Neon PostgreSQL connection string format for SQLModel"
- "SQLModel migrations with Alembic for Neon"
- "Neon serverless-specific connection pooling"

NOT needed:
- SQL basics (SELECT, INSERT, UPDATE) - standard knowledge
- Database normalization - fundamental concept
```

## Query Workflow in Practice

### Scenario: Implementing Auth System

**Step 1: Setup Better Auth (Frontend)**
```
Query: "Better Auth setup for Next.js 16 App Router with JWT"
Read: Installation, configuration file structure, environment variables
Implement: auth.ts config, auth route handler
```

**Step 2: Backend JWT Verification**
```
Query: "FastAPI JWT verification using python-jose Better Auth tokens"
Read: JWT decode, signature verification, dependency injection
Implement: JWT dependency, get_current_user function
```

**Step 3: Protected Endpoints**
```
Query: "FastAPI route dependencies with JWT authentication"
Read: Dependency injection patterns, error handling
Implement: Protected CRUD endpoints with user_id filtering
```

**Step 4: Frontend Integration**
```
Query: "Better Auth React hooks for auth state management"
Read: useSession, signIn, signOut hooks
Implement: Login form, auth context, protected routes
```

## Integration with Other Skills

This skill is **referenced by all other skills** as a fallback:

```markdown
# In nextjs-16-app-router/SKILL.md
When you need current Next.js 16 specifics beyond this skill's scope, 
use the `using-context7` skill to query official documentation.

# In fastapi-async-patterns/SKILL.md
For FastAPI patterns not covered here or when uncertain about current APIs,
consult the `using-context7` skill for official documentation.
```

## Red Flags: When You're Over-Querying

🚩 **Querying for the same topic multiple times in one session**
   → Cache knowledge from first query, reference it

🚩 **Querying before attempting implementation**
   → Try first, query if you hit uncertainty

🚩 **Querying for basic syntax or concepts**
   → Trust your training data for fundamentals

🚩 **Querying without specific framework + version**
   → Refine query to be more specific

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│ QUERY CONTEXT7 IF:                                      │
├─────────────────────────────────────────────────────────┤
│ ✓ Framework-specific (Next.js 16, Better Auth, etc.)   │
│ ✓ Recent version (after Jan 2025 training cutoff)      │
│ ✓ Configuration/setup details                          │
│ ✓ Breaking changes or new APIs                         │
│ ✓ Official best practices                              │
│ ✓ Edge cases in specialized domains                    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ DON'T QUERY CONTEXT7 FOR:                               │
├─────────────────────────────────────────────────────────┤
│ ✗ Basic language syntax                                │
│ ✗ General programming concepts                         │
│ ✗ Well-known patterns                                  │
│ ✗ Information already in conversation                  │
│ ✗ Obvious implementations                              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ QUERY FORMAT:                                           │
├─────────────────────────────────────────────────────────┤
│ [Framework + Version] + [Specific Feature] + [Context]  │
│                                                         │
│ Example:                                                │
│ "Next.js 16 App Router middleware for JWT auth with    │
│  Better Auth token verification"                       │
└─────────────────────────────────────────────────────────┘
```

## Related Skill Files

- `reference.md` - Context7 query syntax and patterns
- `examples.md` - Real-world query examples for Phase 2
- `when-not-to-query.md` - Anti-patterns and over-querying examples

---

**Remember**: Context7 is your connection to **current, official documentation**. Use it strategically for framework-specific knowledge, not as a replacement for your existing expertise in fundamental programming concepts.