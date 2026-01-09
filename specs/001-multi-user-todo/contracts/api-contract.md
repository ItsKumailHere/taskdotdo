# API Contract: Multi-User Todo Application

## Authentication API

### POST /api/auth/register
Register a new user account

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "username": "johndoe"
}
```

**Response (201 Created)**:
```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2026-01-04T10:00:00Z"
}
```

### POST /api/auth/login
Authenticate user and return session token

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "email": "user@example.com",
    "username": "johndoe"
  }
}
```

### POST /api/auth/logout
Logout user and invalidate session

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response (200 OK)**:
```json
{
  "message": "Successfully logged out"
}
```

## User API

### GET /api/users/me
Get current user's profile

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response (200 OK)**:
```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2026-01-04T10:00:00Z",
  "last_login_at": "2026-01-04T09:30:00Z",
  "preferences": {
    "theme": "light"
  }
}
```

### PUT /api/users/me/preferences
Update user preferences

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request**:
```json
{
  "theme": "dark"
}
```

**Response (200 OK)**:
```json
{
  "theme": "dark"
}
```

## Todo API

### GET /api/todos
Get all todos for the current user

**Headers**:
```
Authorization: Bearer {access_token}
```

**Query Parameters**:
- `completed`: boolean (optional) - Filter by completion status
- `category_id`: UUID (optional) - Filter by category
- `limit`: integer (optional, default: 50) - Number of results to return
- `offset`: integer (optional, default: 0) - Number of results to skip

**Response (200 OK)**:
```json
{
  "todos": [
    {
      "id": "b1c2d3e4-f5g6-7890-2345-67890abcdef1",
      "description": "Complete project proposal",
      "due_date": "2026-01-15T10:00:00Z",
      "completed": false,
      "completed_at": null,
      "created_at": "2026-01-04T10:00:00Z",
      "updated_at": "2026-01-04T10:00:00Z",
      "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "category_id": "c1d2e3f4-g5h6-7890-3456-7890abcdef12",
      "tags": [
        {
          "id": "d1e2f3g4-h5i6-7890-4567-890abcdef123",
          "name": "work"
        }
      ]
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### POST /api/todos
Create a new todo

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request**:
```json
{
  "description": "Complete project proposal",
  "due_date": "2026-01-15T10:00:00Z",
  "category_id": "c1d2e3f4-g5h6-7890-3456-7890abcdef12",
  "tag_ids": [
    "d1e2f3g4-h5i6-7890-4567-890abcdef123"
  ]
}
```

**Response (201 Created)**:
```json
{
  "id": "b1c2d3e4-f5g6-7890-2345-67890abcdef1",
  "description": "Complete project proposal",
  "due_date": "2026-01-15T10:00:00Z",
  "completed": false,
  "completed_at": null,
  "created_at": "2026-01-04T10:00:00Z",
  "updated_at": "2026-01-04T10:00:00Z",
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "category_id": "c1d2e3f4-g5h6-7890-3456-7890abcdef12",
  "tags": [
    {
      "id": "d1e2f3g4-h5i6-7890-4567-890abcdef123",
      "name": "work"
    }
  ]
}
```

### GET /api/todos/{id}
Get a specific todo

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response (200 OK)**:
```json
{
  "id": "b1c2d3e4-f5g6-7890-2345-67890abcdef1",
  "description": "Complete project proposal",
  "due_date": "2026-01-15T10:00:00Z",
  "completed": false,
  "completed_at": null,
  "created_at": "2026-01-04T10:00:00Z",
  "updated_at": "2026-01-04T10:00:00Z",
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "category_id": "c1d2e3f4-g5h6-7890-3456-7890abcdef12",
  "tags": [
    {
      "id": "d1e2f3g4-h5i6-7890-4567-890abcdef123",
      "name": "work"
    }
  ]
}
```

### PUT /api/todos/{id}
Update a specific todo

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request**:
```json
{
  "description": "Complete project proposal - Updated",
  "due_date": "2026-01-20T10:00:00Z",
  "completed": true,
  "category_id": "c1d2e3f4-g5h6-7890-3456-7890abcdef12",
  "tag_ids": [
    "d1e2f3g4-h5i6-7890-4567-890abcdef123",
    "e1f2g3h4-i5j6-7890-5678-90abcdef1234"
  ]
}
```

**Response (200 OK)**:
```json
{
  "id": "b1c2d3e4-f5g6-7890-2345-67890abcdef1",
  "description": "Complete project proposal - Updated",
  "due_date": "2026-01-20T10:00:00Z",
  "completed": true,
  "completed_at": "2026-01-04T11:30:00Z",
  "created_at": "2026-01-04T10:00:00Z",
  "updated_at": "2026-01-04T11:30:00Z",
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "category_id": "c1d2e3f4-g5h6-7890-3456-7890abcdef12",
  "tags": [
    {
      "id": "d1e2f3g4-h5i6-7890-4567-890abcdef123",
      "name": "work"
    },
    {
      "id": "e1f2g3h4-i5j6-7890-5678-90abcdef1234",
      "name": "urgent"
    }
  ]
}
```

### DELETE /api/todos/{id}
Delete a specific todo

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response (204 No Content)**

## Category API

### GET /api/categories
Get all categories for the current user

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response (200 OK)**:
```json
{
  "categories": [
    {
      "id": "c1d2e3f4-g5h6-7890-3456-7890abcdef12",
      "name": "Work",
      "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "created_at": "2026-01-04T10:00:00Z"
    }
  ]
}
```

### POST /api/categories
Create a new category

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request**:
```json
{
  "name": "Personal"
}
```

**Response (201 Created)**:
```json
{
  "id": "d1e2f3g4-h5i6-7890-4567-890abcdef123",
  "name": "Personal",
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "created_at": "2026-01-04T10:00:00Z"
}
```

## Tag API

### GET /api/tags
Get all tags for the current user

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response (200 OK)**:
```json
{
  "tags": [
    {
      "id": "d1e2f3g4-h5i6-7890-4567-890abcdef123",
      "name": "work",
      "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "created_at": "2026-01-04T10:00:00Z"
    }
  ]
}
```

### POST /api/tags
Create a new tag

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request**:
```json
{
  "name": "important"
}
```

**Response (201 Created)**:
```json
{
  "id": "e1f2g3h4-i5j6-7890-5678-90abcdef1234",
  "name": "important",
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "created_at": "2026-01-04T10:00:00Z"
}
```