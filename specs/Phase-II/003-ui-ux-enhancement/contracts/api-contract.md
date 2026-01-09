# API Contract: Responsive UI/UX Enhancement & Task Management

**Feature**: Responsive UI/UX Enhancement & Task Management
**Date**: 2026-01-09
**Location**: /specs/Phase-II/003-ui-ux-enhancement/contracts/

## Task Management API Extensions

### GET /api/v1/todos (Extended)
Retrieve all tasks for the authenticated user with filtering, sorting, and search capabilities

**Authentication Required**: Bearer token

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Query Parameters**:
- `status` (optional): Filter by task status ("all", "pending", "completed") - defaults to "all"
- `sort_by` (optional): Sort by field ("created_at", "title", "due_date") - defaults to "created_at"
- `order` (optional): Sort order ("asc", "desc") - defaults to "desc"
- `search` (optional): Search term to match against title and description
- `page` (optional): Page number for pagination - defaults to 1
- `limit` (optional): Number of items per page - defaults to 20

**Request Example**:
```
GET /api/v1/todos?status=pending&sort_by=due_date&order=asc&search=meeting&page=1&limit=10
Authorization: Bearer {access_token}
```

**Responses**:
- `200 OK`: Tasks successfully retrieved
  ```json
  {
    "data": [
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
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "pages": 3
    }
  }
  ```
- `400 Bad Request`: Invalid query parameters
- `401 Unauthorized`: Invalid or expired token

## User Preferences API

### GET /api/v1/users/preferences
Retrieve the authenticated user's preferences including theme settings

**Authentication Required**: Bearer token

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Responses**:
- `200 OK`: User preferences successfully retrieved
  ```json
  {
    "theme": "string (light|dark|auto)",
    "language": "string (en|es|fr|etc.)",
    "timezone": "string (IANA timezone identifier)",
    "notifications_enabled": "boolean",
    "dashboard_layout": "string (default|compact|focus)"
  }
  ```
- `401 Unauthorized`: Invalid or expired token

### PUT /api/v1/users/preferences
Update the authenticated user's preferences

**Authentication Required**: Bearer token

**Request Headers**:
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "theme": "string (light|dark|auto)",
  "language": "string (optional)",
  "timezone": "string (optional)",
  "notifications_enabled": "boolean (optional)",
  "dashboard_layout": "string (optional)"
}
```

**Responses**:
- `200 OK`: User preferences successfully updated
  ```json
  {
    "theme": "string (light|dark|auto)",
    "language": "string",
    "timezone": "string",
    "notifications_enabled": "boolean",
    "dashboard_layout": "string"
  }
  ```
- `400 Bad Request`: Invalid preference values
- `401 Unauthorized`: Invalid or expired token