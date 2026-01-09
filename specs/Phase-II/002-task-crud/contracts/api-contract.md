# API Contract: Task CRUD Operations

**Feature**: Task CRUD Operations
**Date**: 2026-01-09
**Location**: /specs/Phase-II/002-task-crud/contracts/

## Task API Endpoints

### POST /api/v1/todos
Create a new task for the authenticated user

**Authentication Required**: Bearer token

**Request Headers**:
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "string (required, 1-255 characters)",
  "description": "string (optional, max 1000 characters)",
  "due_date": "string (optional, ISO 8601 datetime format)"
}
```

**Responses**:
- `201 Created`: Task successfully created
  ```json
  {
    "id": "string (UUID)",
    "title": "string",
    "description": "string (nullable)",
    "status": "string (pending|completed)",
    "due_date": "string (ISO 8601 datetime, nullable)",
    "user_id": "string (UUID)",
    "created_at": "string (ISO 8601 datetime)",
    "updated_at": "string (ISO 8601 datetime, nullable)"
  }
  ```
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `422 Unprocessable Entity`: Validation error

### GET /api/v1/todos
Retrieve all tasks for the authenticated user

**Authentication Required**: Bearer token

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Query Parameters**:
- `status` (optional): Filter by status (pending|completed)
- `sort_by` (optional): Sort by field (created_at|due_date|title) [default: created_at]
- `sort_order` (optional): Sort order (asc|desc) [default: desc]
- `page` (optional): Page number [default: 1]
- `page_size` (optional): Number of items per page [default: 10, max: 100]

**Responses**:
- `200 OK`: Tasks retrieved successfully
  ```json
  {
    "tasks": [
      {
        "id": "string (UUID)",
        "title": "string",
        "description": "string (nullable)",
        "status": "string (pending|completed)",
        "due_date": "string (ISO 8601 datetime, nullable)",
        "user_id": "string (UUID)",
        "created_at": "string (ISO 8601 datetime)",
        "updated_at": "string (ISO 8601 datetime, nullable)"
      }
    ],
    "total": "integer",
    "page": "integer",
    "page_size": "integer"
  }
  ```
- `401 Unauthorized`: Invalid or expired token

### GET /api/v1/todos/{id}
Retrieve a specific task by ID

**Authentication Required**: Bearer token

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Path Parameter**:
- `id`: Task ID (UUID)

**Responses**:
- `200 OK`: Task retrieved successfully
  ```json
  {
    "id": "string (UUID)",
    "title": "string",
    "description": "string (nullable)",
    "status": "string (pending|completed)",
    "due_date": "string (ISO 8601 datetime, nullable)",
    "user_id": "string (UUID)",
    "created_at": "string (ISO 8601 datetime)",
    "updated_at": "string (ISO 8601 datetime, nullable)"
  }
  ```
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: Task does not belong to the user
- `404 Not Found`: Task not found

### PUT /api/v1/todos/{id}
Update an existing task

**Authentication Required**: Bearer token

**Request Headers**:
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Path Parameter**:
- `id`: Task ID (UUID)

**Request Body** (all fields optional):
```json
{
  "title": "string (optional, 1-255 characters)",
  "description": "string (optional, max 1000 characters)",
  "status": "string (optional, pending|completed)",
  "due_date": "string (optional, ISO 8601 datetime format)"
}
```

**Responses**:
- `200 OK`: Task updated successfully
  ```json
  {
    "id": "string (UUID)",
    "title": "string",
    "description": "string (nullable)",
    "status": "string (pending|completed)",
    "due_date": "string (ISO 8601 datetime, nullable)",
    "user_id": "string (UUID)",
    "created_at": "string (ISO 8601 datetime)",
    "updated_at": "string (ISO 8601 datetime, nullable)"
  }
  ```
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: Task does not belong to the user
- `404 Not Found`: Task not found
- `422 Unprocessable Entity`: Validation error

### DELETE /api/v1/todos/{id}
Delete a specific task

**Authentication Required**: Bearer token

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Path Parameter**:
- `id`: Task ID (UUID)

**Responses**:
- `204 No Content`: Task deleted successfully
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: Task does not belong to the user
- `404 Not Found`: Task not found

### PATCH /api/v1/todos/{id}/status
Update the status of a specific task

**Authentication Required**: Bearer token

**Request Headers**:
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Path Parameter**:
- `id`: Task ID (UUID)

**Request Body**:
```json
{
  "status": "string (required, pending|completed)"
}
```

**Responses**:
- `200 OK`: Task status updated successfully
  ```json
  {
    "id": "string (UUID)",
    "title": "string",
    "description": "string (nullable)",
    "status": "string (pending|completed)",
    "due_date": "string (ISO 8601 datetime, nullable)",
    "user_id": "string (UUID)",
    "created_at": "string (ISO 8601 datetime)",
    "updated_at": "string (ISO 8601 datetime, nullable)"
  }
  ```
- `400 Bad Request`: Invalid status value
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: Task does not belong to the user
- `404 Not Found`: Task not found
- `422 Unprocessable Entity`: Validation error