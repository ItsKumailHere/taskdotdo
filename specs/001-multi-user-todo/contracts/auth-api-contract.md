# API Contract: Authentication Service

**Feature**: User Authentication & Authorization
**Date**: 2026-01-07

## Authentication API Endpoints

### User Registration
- **Endpoint**: `POST /api/auth/register`
- **Description**: Registers a new user account
- **Authentication**: None required
- **Request Body**:
  ```json
  {
    "email": "string (required, valid email format)",
    "password": "string (min 6 characters)",
    "name": "string (required)"
  }
  ```
- **Responses**:
  - `201 Created`: User successfully registered
    ```json
    {
      "id": "string (user ID)",
      "email": "string",
      "name": "string",
      "createdAt": "datetime"
    }
    ```
  - `400 Bad Request`: Invalid input data
  - `409 Conflict`: Email already exists

### User Login
- **Endpoint**: `POST /api/auth/login`
- **Description**: Authenticates user and returns JWT tokens
- **Authentication**: None required
- **Request Body**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required)"
  }
  ```
- **Responses**:
  - `200 OK`: Login successful
    ```json
    {
      "accessToken": "string (JWT token)",
      "refreshToken": "string (refresh token)",
      "user": {
        "id": "string",
        "email": "string",
        "name": "string"
      }
    }
    ```
  - `400 Bad Request`: Invalid input
  - `401 Unauthorized`: Invalid credentials

### User Logout
- **Endpoint**: `POST /api/auth/logout`
- **Description**: Logs out the current user
- **Authentication**: Bearer token required
- **Request Headers**:
  - `Authorization: Bearer {accessToken}`
- **Responses**:
  - `200 OK`: Successfully logged out
  - `401 Unauthorized`: Invalid or expired token

### Get Current User
- **Endpoint**: `GET /api/auth/me`
- **Description**: Retrieves information about the authenticated user
- **Authentication**: Bearer token required
- **Request Headers**:
  - `Authorization: Bearer {accessToken}`
- **Responses**:
  - `200 OK`: User data retrieved
    ```json
    {
      "id": "string",
      "email": "string",
      "name": "string",
      "createdAt": "datetime",
      "lastLoginAt": "datetime"
    }
    ```
  - `401 Unauthorized`: Invalid or expired token

### Refresh Token
- **Endpoint**: `POST /api/auth/refresh`
- **Description**: Refreshes the access token using a refresh token
- **Request Body**:
  ```json
  {
    "refreshToken": "string (required)"
  }
  ```
- **Responses**:
  - `200 OK`: Token refreshed successfully
    ```json
    {
      "accessToken": "string (new JWT token)"
    }
    ```
  - `400 Bad Request`: Invalid refresh token
  - `401 Unauthorized`: Expired or invalid refresh token

### Protected Todo Endpoints
- **Endpoint**: `GET /api/todos`
- **Description**: Retrieves todos for the authenticated user
- **Authentication**: Bearer token required
- **Request Headers**:
  - `Authorization: Bearer {accessToken}`
- **Responses**:
  - `200 OK`: List of user's todos
    ```json
    [
      {
        "id": "integer",
        "title": "string",
        "description": "string",
        "completed": "boolean",
        "userId": "string",
        "createdAt": "datetime",
        "updatedAt": "datetime"
      }
    ]
    ```
  - `401 Unauthorized`: Invalid or expired token