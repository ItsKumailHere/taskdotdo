---
name: fullstack-integration
description: Governs integration between Next.js 16 frontend and FastAPI backend. Use when connecting APIs, handling JWT auth, configuring CORS, or debugging cross-stack issues.
---

# Full-Stack Integration Skill

This Skill defines **how frontend and backend talk to each other**.

## Core Architecture

Frontend (Next.js 16)
→ Better Auth
→ JWT
→ FastAPI
→ SQLModel
→ Neon PostgreSQL

## Non-Negotiable Rules

1. Frontend never stores JWT manually
2. Backend trusts JWT only after verification
3. Every request is user-scoped
4. CORS is explicit and locked down

See:
- [auth-flow.md](auth-flow.md)
- [api-client.md](api-client.md)
- [cors-and-deployment.md](cors-and-deployment.md)
- [error-handling.md](error-handling.md)

---

## Context7 Usage

Use Context7 when:
- Verifying Better Auth token format
- FastAPI dependency injection edge cases
- Vercel deployment behavior

Good queries:
- “FastAPI JWT dependency async example”
- “Better Auth JWT verification server side”
