# User Authentication & Authorization Documentation

This document provides detailed information about the user authentication and authorization feature implemented in the TaskDo application.

## Overview

The authentication system provides secure user registration, login, and session management using JWT tokens. It ensures that only authenticated users can access protected resources and perform authorized actions.

## Architecture

### Backend Components

1. **Models** (`backend/app/models/user.py`):
   - Defines the User model with fields like email, password hash, etc.
   - Implements proper security measures for password storage

2. **Schemas** (`backend/app/schemas/auth.py`):
   - Request/response schemas for registration and login
   - JWT token schemas for authentication

3. **Services** (`backend/app/services/user_service.py`, `backend/app/services/auth_service.py`):
   - Business logic for user management
   - Password hashing and verification
   - JWT token generation and validation

4. **API Routes** (`backend/app/api/v1/auth.py`):
   - Registration endpoint: `POST /api/auth/register`
   - Login endpoint: `POST /api/auth/login`
   - Logout endpoint: `POST /api/auth/logout`
   - Token refresh endpoint: `POST /api/auth/refresh`

5. **Utilities** (`backend/app/utils/jwt.py`):
   - JWT token creation and validation utilities
   - Token expiration handling

6. **Middleware** (`backend/app/middleware/auth.py`):
   - Authentication middleware for protecting routes
   - Token validation for incoming requests

### Frontend Components

1. **Pages** (`frontend/app/register/page.tsx`, `frontend/app/login/page.tsx`):
   - Registration and login forms
   - Navigation and user feedback

2. **Components** (`frontend/components/auth/`):
   - Reusable authentication forms and UI elements
   - Protected route components

3. **Utilities** (`frontend/lib/auth.ts`, `frontend/lib/api.ts`):
   - Authentication state management
   - API request utilities with authentication headers
   - Route protection logic

## API Endpoints

### Registration
- **Endpoint**: `POST /api/auth/register`
- **Request Body**: `{ email: string, password: string, name?: string }`
- **Response**: `{ access_token: string, token_type: string }`
- **Description**: Creates a new user account and returns an authentication token

### Login
- **Endpoint**: `POST /api/auth/login`
- **Request Body**: `{ email: string, password: string }`
- **Response**: `{ access_token: string, token_type: string }`
- **Description**: Authenticates a user and returns an authentication token

### Logout
- **Endpoint**: `POST /api/auth/logout`
- **Request Headers**: `Authorization: Bearer {token}`
- **Response**: `{ message: string }`
- **Description**: Invalidates the user's session

### Token Refresh
- **Endpoint**: `POST /api/auth/refresh`
- **Request Headers**: `Authorization: Bearer {refresh_token}`
- **Response**: `{ access_token: string, token_type: string }`
- **Description**: Generates a new access token using a refresh token

## Security Measures

1. **Password Security**:
   - Passwords are hashed using bcrypt
   - Minimum password strength requirements enforced

2. **JWT Security**:
   - Tokens have configurable expiration times
   - Secure signing algorithm (HS256/RS256)
   - Proper token storage and transmission

3. **Rate Limiting**:
   - Protection against brute force attacks
   - Limit on authentication attempts

4. **Input Validation**:
   - All inputs are validated and sanitized
   - Prevention of injection attacks

## Implementation Notes

### Password Handling
- Passwords are never stored in plain text
- bcrypt is used for password hashing with appropriate salt
- Password strength validation is implemented

### Token Management
- Access tokens have short expiration times
- Refresh tokens have longer expiration times
- Secure token storage (preferably httpOnly cookies)

### Session Management
- Proper logout functionality that invalidates tokens
- Automatic token refresh when possible
- Clear session handling on client-side

## Testing Strategy

### Backend Tests
- Unit tests for authentication services
- Integration tests for API endpoints
- Contract tests for API compliance

### Frontend Tests
- Component tests for authentication UI
- Integration tests for authentication flows
- End-to-end tests for complete user journeys

## Error Handling

Common authentication errors and their handling:

- **Invalid Credentials**: Return 401 Unauthorized with appropriate message
- **Token Expiration**: Return 401 Unauthorized, prompt for re-authentication
- **Invalid Token**: Return 401 Unauthorized
- **Rate Limit Exceeded**: Return 429 Too Many Requests
- **Validation Errors**: Return 422 Unprocessable Entity with validation details

## Future Enhancements

- Two-factor authentication (2FA)
- Social login integration
- Password reset functionality
- Account verification via email
- Session management across multiple devices