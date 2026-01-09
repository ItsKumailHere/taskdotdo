# Authentication Flow

## Frontend
1. Better Auth handles login
2. JWT issued client-side
3. JWT attached automatically to requests

## Request
Authorization: Bearer <token>

## Backend
1. Extract Authorization header
2. Verify JWT using BETTER_AUTH_SECRET
3. Extract `user_id`
4. Scope all queries by `user_id`

JWT is never optional.
