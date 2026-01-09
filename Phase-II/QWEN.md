## SKILLS System

The SKILLS system provides specialized knowledge for implementing features in this project. SKILLS are stored in the `.qwen/skills/` directory and contain detailed information about specific technologies and implementation patterns.

### Using SKILLS

- SKILLS are located in `@.qwen/skills/**` directory
- Each skill has a main `SKILL.md` file with comprehensive knowledge about a specific technology
- Some skills include additional files (examples.md, reference.md, etc.) with specific implementation details
- SKILLS are designed specifically for Phase II of the Hackathon to ensure consistent implementation patterns

### Available SKILLS

- `better-auth-jwt` - Better Auth setup with JWT token flow for Next.js 16 and FastAPI
- `fastapi-async-patterns` - FastAPI async endpoint patterns, dependency injection, and API design
- `frontend-design` - Frontend interface creation with distinctive, production-grade design
- `fullstack-integration` - Integration patterns between Next.js 16 frontend and FastAPI backend
- `nextjs-16-app-router` - Next.js 16 App Router usage, Server vs Client Components
- `sqlmodel-database` - SQLModel ORM patterns for async PostgreSQL operations with Neon
- `using-context7` - Using Context7 for current documentation on modern frameworks

### SKILLS for Agents

All specialized agents (backend-dev, database-architect, frontend-dev, integration-specialist) must be given access to these SKILLS to ensure consistent implementation patterns across all code components. When using the `task` tool to delegate work to agents, they will leverage the appropriate SKILLS for their specialized areas.