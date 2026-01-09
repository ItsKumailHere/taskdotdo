# Task CRUD Operations Documentation

This document provides detailed information about the task management system with CRUD operations implemented in the TaskDo application.

## Overview

The task management system allows authenticated users to create, read, update, and delete tasks. It provides a complete task lifecycle management solution with status tracking, filtering, and sorting capabilities.

## Architecture

### Backend Components

1. **Models** (`backend/app/models/todo.py`):
   - Defines the Todo model with fields like title, description, status, due date, etc.
   - Implements relationships with the User model
   - Includes proper validation and constraints

2. **Schemas** (`backend/app/schemas/todo.py`):
   - Request/response schemas for task operations
   - Validation rules for task data
   - Public representation of tasks

3. **Services** (`backend/app/services/todo_service.py`):
   - Business logic for task operations
   - User authorization checks
   - Data validation and processing

4. **API Routes** (`backend/app/api/v1/todos.py`):
   - Task CRUD endpoints: `POST /api/v1/todos`, `GET /api/v1/todos`, `PUT /api/v1/todos/{id}`, `DELETE /api/v1/todos/{id}`
   - Status update endpoint: `PATCH /api/v1/todos/{id}/status`
   - Filtering and pagination support

5. **Database** (`backend/app/database/`):
   - Todo table schema and migrations
   - Indexes for efficient querying
   - Relationship management with User model

### Frontend Components

1. **Pages** (`frontend/app/dashboard/page.tsx`, `frontend/app/tasks/page.tsx`):
   - Dashboard page showing user's tasks
   - Task list page with filtering options

2. **Components** (`frontend/components/tasks/`):
   - Reusable task components for display and interaction
   - Task form for creation and editing
   - Task filter and sort controls

3. **Utilities** (`frontend/lib/api/todo-api.ts`, `frontend/lib/types/todo.ts`):
   - API client for task operations
   - Type definitions for task data
   - Error handling and response processing

## API Endpoints

### Create Task
- **Endpoint**: `POST /api/v1/todos`
- **Request Body**: `{ title: string, description?: string, due_date?: string }`
- **Response**: `{ id: string, title: string, description?: string, status: "pending"|"completed", due_date?: string, user_id: string, created_at: string, updated_at?: string }`
- **Description**: Creates a new task for the authenticated user

### Get All Tasks
- **Endpoint**: `GET /api/v1/todos`
- **Query Parameters**: `status`, `sort_by`, `sort_order`, `page`, `page_size`
- **Response**: `{ tasks: Array<Task>, total: number, page: number, page_size: number }`
- **Description**: Retrieves all tasks for the authenticated user with optional filtering and pagination

### Get Single Task
- **Endpoint**: `GET /api/v1/todos/{id}`
- **Response**: `Task`
- **Description**: Retrieves a specific task by ID

### Update Task
- **Endpoint**: `PUT /api/v1/todos/{id}`
- **Request Body**: Partial `{ title?: string, description?: string, status?: "pending"|"completed", due_date?: string }`
- **Response**: Updated `Task`
- **Description**: Updates an existing task

### Delete Task
- **Endpoint**: `DELETE /api/v1/todos/{id}`
- **Response**: `204 No Content`
- **Description**: Deletes a task by ID

### Update Task Status
- **Endpoint**: `PATCH /api/v1/todos/{id}/status`
- **Request Body**: `{ status: "pending"|"completed" }`
- **Response**: Updated `Task`
- **Description**: Updates the status of a task

## Security Measures

1. **Authentication**:
   - All endpoints require a valid JWT token
   - Tokens are validated against the authentication system
   - Expired tokens are rejected

2. **Authorization**:
   - Users can only access their own tasks
   - Task ownership is verified on each request
   - Unauthorized access attempts are logged

3. **Input Validation**:
   - All inputs are validated on both frontend and backend
   - Sanitization is applied to prevent XSS attacks
   - Length and format constraints are enforced

## Features

### Task Management
- Create new tasks with title, description, and due date
- View all tasks with filtering by status
- Update task details as needed
- Delete tasks that are no longer needed
- Mark tasks as complete/incomplete

### Filtering and Sorting
- Filter tasks by status (all, pending, completed)
- Sort tasks by creation date, title, or due date
- Pagination for large task lists

### User Experience
- Responsive design for all device sizes
- Loading states during API operations
- Error handling and user feedback
- Optimistic updates for better responsiveness

## Error Handling

### Backend Error Responses
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### Frontend Error Handling
- User-friendly error messages
- Retry mechanisms for failed requests
- Graceful degradation when offline
- Loading indicators during operations

## Performance Considerations

### Database Optimization
- Proper indexing on user_id, status, and due_date
- Efficient queries with appropriate joins
- Pagination for large datasets

### Frontend Performance
- Virtual scrolling for large task lists
- Memoization of components
- Lazy loading of data
- Caching of API responses

## Testing

### Backend Tests
- Unit tests for service layer functions
- Integration tests for API endpoints
- Authentication and authorization tests
- Database transaction tests

### Frontend Tests
- Component tests for UI elements
- Integration tests for API interactions
- End-to-end tests for user workflows
- Accessibility tests

## Deployment

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret
- `NEXT_PUBLIC_BACKEND_API_URL`: Backend API URL for frontend

### Scaling Considerations
- Database connection pooling
- API rate limiting
- CDN for static assets
- Horizontal scaling capabilities