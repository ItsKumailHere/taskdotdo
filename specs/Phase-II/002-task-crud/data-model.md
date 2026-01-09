# Data Model: Task CRUD Operations

**Feature**: Task CRUD Operations
**Date**: 2026-01-09
**Location**: /specs/Phase-II/002-task-crud/

## Database Schema

### Todos Table

```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    due_date TIMESTAMP WITH TIME ZONE,
    user_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_todos_user_id (user_id),
    INDEX idx_todos_status (status),
    INDEX idx_todos_due_date (due_date),
    INDEX idx_todos_created_at (created_at)
);
```

### Relationships
- `todos.user_id` references `users.id` (many-to-one relationship)
- When a user is deleted, all their tasks are automatically deleted (CASCADE)

## SQLModel Definitions

### Task Status Enum

```python
import enum

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
```

### Todo Model

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

class TodoCreate(TodoBase):
    """Schema for creating a new todo"""
    title: str = Field(min_length=1, max_length=255)
    pass

class TodoUpdate(SQLModel):
    """Schema for updating an existing todo"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[TaskStatus] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)

class TodoPublic(TodoBase):
    """Public representation of a todo (with ID and timestamps)"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
```

## Indexing Strategy

### Required Indexes
1. `idx_todos_user_id` - For efficient querying of user-specific tasks
2. `idx_todos_status` - For filtering by task status
3. `idx_todos_due_date` - For sorting and filtering by due date
4. `idx_todos_created_at` - For chronological ordering

### Query Performance Considerations
- Queries filtered by user_id will be efficient due to index
- Combined filters (user_id + status) will benefit from index intersection
- Sorting by due_date or created_at will be efficient

## API Response Models

### Todo Response Schema

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import enum

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TodoResponse(BaseModel):
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

### Todo List Response Schema

```python
from pydantic import BaseModel
from typing import List

class TodoListResponse(BaseModel):
    tasks: List[TodoResponse]
    total: int
    page: int
    page_size: int
```

## Validation Rules

### Field Validations
1. `title`: Required, 1-255 characters
2. `description`: Optional, max 1000 characters
3. `status`: Must be either "pending" or "completed"
4. `due_date`: Optional, must be a valid datetime
5. `user_id`: Required, must reference an existing user

### Business Logic Validations
1. Users can only access their own tasks
2. Due dates should not be in the past when marking as completed (optional rule)
3. Prevent duplicate titles for the same user (optional rule)

## Migration Strategy

### Initial Migration
```sql
-- Create todos table
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    due_date TIMESTAMP WITH TIME ZONE,
    user_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_status ON todos(status);
CREATE INDEX idx_todos_due_date ON todos(due_date);
CREATE INDEX idx_todos_created_at ON todos(created_at);
```

### Future Migration Considerations
- Adding category/tags support
- Adding priority levels
- Adding recurrence patterns
- Adding attachments or file uploads