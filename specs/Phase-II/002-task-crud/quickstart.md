# Quickstart Guide: Task CRUD Operations

**Feature**: Task CRUD Operations
**Date**: 2026-01-09
**Location**: /specs/Phase-II/002-task-crud/

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or Neon Serverless Postgres)
- Next.js 16+
- Completed User Authentication & Authorization feature

## Setup Instructions

### Backend Setup (FastAPI)

1. Install dependencies (if not already installed):
```bash
pip install fastapi sqlmodel python-jose[cryptography] passlib[bcrypt] python-multipart
```

2. Create the Todo model in `backend/app/models/todo.py`:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
import enum

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    due_date: Optional[datetime] = Field(default=None)

class Todo(TodoBase, table=True):
    __tablename__ = "todos"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationship to user
    user: "User" = Relationship(back_populates="todos")
```

3. Create Todo schemas in `backend/app/schemas/todo.py`:
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import enum

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None

class TodoPublic(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    due_date: Optional[datetime]
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
```

4. Set up Todo API endpoints in `backend/app/api/v1/todos.py`:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from ...database.session import get_session
from ...models.todo import Todo, TodoCreate, TodoUpdate, TaskStatus
from ...schemas.todo import TodoPublic
from ...auth.jwt import get_current_user
from ...models.user import User

router = APIRouter()

@router.get("/", response_model=List[TodoPublic])
async def get_todos(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get all todos for the current user."""
    # Implementation here
    pass

@router.post("/", response_model=TodoPublic)
async def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new todo for the current user."""
    # Implementation here
    pass

@router.get("/{todo_id}", response_model=TodoPublic)
async def get_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific todo by ID."""
    # Implementation here
    pass

@router.put("/{todo_id}", response_model=TodoPublic)
async def update_todo(
    todo_id: str,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update a specific todo by ID."""
    # Implementation here
    pass

@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a specific todo by ID."""
    # Implementation here
    pass

@router.patch("/{todo_id}/status")
async def update_todo_status(
    todo_id: str,
    status: TaskStatus,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update the status of a specific todo."""
    # Implementation here
    pass
```

### Frontend Setup (Next.js 16)

1. Create Todo type definitions in `frontend/lib/types/todo.ts`:
```typescript
export enum TaskStatus {
  PENDING = 'pending',
  COMPLETED = 'completed'
}

export interface Todo {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  due_date?: string; // ISO string
  user_id: string;
  created_at: string; // ISO string
  updated_at?: string; // ISO string
}

export interface CreateTodoData {
  title: string;
  description?: string;
  due_date?: string; // ISO string
}

export interface UpdateTodoData {
  title?: string;
  description?: string;
  status?: TaskStatus;
  due_date?: string; // ISO string
}
```

2. Create Todo API client in `frontend/lib/api/todo-api.ts`:
```typescript
import { apiClient } from './client';
import { Todo, CreateTodoData, UpdateTodoData } from '../types/todo';

class TodoApi {
  static async getTodos(): Promise<Todo[]> {
    return apiClient.get('/todos');
  }

  static async createTodo(todoData: CreateTodoData): Promise<Todo> {
    return apiClient.post('/todos', todoData);
  }

  static async updateTodo(id: string, todoData: UpdateTodoData): Promise<Todo> {
    return apiClient.put(`/todos/${id}`, todoData);
  }

  static async deleteTodo(id: string): Promise<void> {
    return apiClient.delete(`/todos/${id}`);
  }

  static async updateTodoStatus(id: string, status: 'pending' | 'completed'): Promise<Todo> {
    return apiClient.patch(`/todos/${id}/status`, { status });
  }
}

export default TodoApi;
```

3. Create TaskList component in `frontend/components/tasks/TaskList.tsx`:
```tsx
import React, { useState, useEffect } from 'react';
import { Todo } from '../../lib/types/todo';
import TodoApi from '../../lib/api/todo-api';
import TaskItem from './TaskItem';

interface TaskListProps {
  filter?: 'all' | 'pending' | 'completed';
}

const TaskList: React.FC<TaskListProps> = ({ filter = 'all' }) => {
  const [tasks, setTasks] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const todos = await TodoApi.getTodos();
        setTasks(todos);
      } catch (error) {
        console.error('Error fetching tasks:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  const filteredTasks = tasks.filter(task => {
    if (filter === 'pending') return task.status === 'pending';
    if (filter === 'completed') return task.status === 'completed';
    return true; // 'all'
  });

  if (loading) return <div>Loading tasks...</div>;

  return (
    <div className="task-list">
      {filteredTasks.map(task => (
        <TaskItem key={task.id} task={task} />
      ))}
    </div>
  );
};

export default TaskList;
```

## Running the Application

### Backend
1. Ensure your database is running and accessible
2. Set up environment variables:
   - `DATABASE_URL` - PostgreSQL connection string
   - `BETTER_AUTH_SECRET` - Secret key for JWT
3. Run the backend server:
```bash
cd Phase-II/backend
uv run uvicorn main:app --reload
```

### Frontend
1. Install dependencies:
```bash
cd Phase-II/frontend
npm install
```
2. Set up environment variables in `.env.local`:
   - `NEXT_PUBLIC_BACKEND_API_URL` - URL of your backend API
3. Run the frontend:
```bash
npm run dev
```

## API Endpoints

### Task Operations
- `GET /api/v1/todos` - Get all user's tasks
- `POST /api/v1/todos` - Create a new task
- `GET /api/v1/todos/{id}` - Get a specific task
- `PUT /api/v1/todos/{id}` - Update a task
- `DELETE /api/v1/todos/{id}` - Delete a task
- `PATCH /api/v1/todos/{id}/status` - Update task status

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer {token}
```

## Testing

### Backend Tests
Run backend tests:
```bash
cd Phase-II/backend
uv run pytest tests/todo/
```

### Frontend Tests
Run frontend tests:
```bash
cd Phase-II/frontend
npm test
```

## Troubleshooting

### Common Issues
1. **Authentication errors**: Ensure you're logged in and the JWT token is properly set in headers
2. **Database connection errors**: Verify your DATABASE_URL is correct and database is running
3. **CORS errors**: Check that your frontend and backend URLs are properly configured in CORS settings
4. **Task access errors**: Verify that users can only access their own tasks