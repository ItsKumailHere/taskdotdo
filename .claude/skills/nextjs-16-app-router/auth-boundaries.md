# Authentication Boundaries

## Allowed
- Server Components
- Middleware
- Route handlers
- Server Actions

## Forbidden
- Client Components
- Browser storage access

## Pattern
Client → Server Component → FastAPI

Client Components receive **data**, never tokens.

If auth is needed:
- Fetch in layout
- Pass data down as props