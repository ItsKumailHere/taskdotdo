# Error Handling

## Backend
- Use HTTPException
- Never leak stack traces
- Consistent error shape

## Frontend
- Server Components handle failures
- Client Components only render state

## Debug Strategy
1. Verify token
2. Verify CORS
3. Verify user_id scoping
