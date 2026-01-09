---
name: fastapi-async-patterns
description: Expert in FastAPI async endpoint patterns, dependency injection, request/response models, error handling, and CORS configuration. Use for all backend API implementations.
---

# FastAPI Async Patterns - Modern Python API Development

You are an expert in FastAPI, the modern, fast (high-performance) Python web framework for building APIs. This skill covers async patterns, dependency injection, request validation, and production-ready API design.

## Core Philosophy

**FastAPI = Speed + Type Safety + Automatic Documentation**

- **Async-first**: All endpoints use `async def` for concurrency
- **Type hints**: Python types for validation and documentation
- **Pydantic models**: Automatic request/response validation
- **Dependency injection**: Clean separation of concerns
- **OpenAPI/Swagger**: Automatic interactive API docs

## When to Use This Skill

✅ **Use this skill for:**
- Defining async API endpoints with proper HTTP methods
- Implementing dependency injection (sessions, auth, config)
- Creating request/response Pydantic models
- Handling errors with HTTPException
- Configuring CORS for frontend integration
- Organizing routes with APIRouter
- Implementing JWT authentication dependencies

❌ **Don't use for:**
- Basic Python syntax - you know this
- HTTP fundamentals (status codes, methods) - standard knowledge
- General async/await concepts - covered in training

## Fundamental Patterns

### 1. FastAPI Application Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create app instance
app = FastAPI(
    title="Todo API",
    description="Full-stack todo application API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Key Concepts:**
- `FastAPI()` creates application instance with metadata
- CORS middleware enables frontend to call API
- `allow_credentials=True` for cookie/auth headers
- Health check endpoint for monitoring

### 2. Async Endpoint Pattern

```python
from fastapi import FastAPI, HTTPException
from typing import List

@app.get("/todos", response_model=List[TodoPublic])
async def get_todos(
    completed: bool | None = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Get all todos with optional filtering.
    
    - **completed**: Filter by completion status
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    # Endpoint logic here
    return todos
```

**Key Concepts:**
- Always use `async def` for endpoints
- Type hints for automatic validation (`completed: bool | None`)
- `response_model` for response validation and documentation
- Docstrings appear in OpenAPI/Swagger docs
- Query parameters with defaults

### 3. Dependency Injection

```python
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

# Database session dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Use dependency in endpoint
@app.get("/todos")
async def get_todos(
    session: AsyncSession = Depends(get_session)
):
    # session is automatically provided
    statement = select(Todo)
    result = await session.exec(statement)
    return result.all()
```

**Key Concepts:**
- `Depends()` injects dependencies automatically
- Dependencies can be async generators (yield)
- Session cleanup handled automatically
- Chain dependencies (dependency can depend on another)

### 4. Request/Response Models

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Request model (for creating)
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False

# Request model (for updating)
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None

# Response model (for returning)
class TodoPublic(BaseModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allow ORM mode

# Use in endpoint
@app.post("/todos", response_model=TodoPublic, status_code=201)
async def create_todo(todo: TodoCreate):
    # todo is automatically validated
    # Return value is automatically validated against TodoPublic
    return new_todo
```

**Key Concepts:**
- Separate models for create/update/response
- `Field()` for validation constraints
- `response_model` excludes internal fields
- `from_attributes=True` for SQLModel compatibility
- Automatic validation and error responses

### 5. Error Handling

```python
from fastapi import HTTPException, status

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: str):
    # Query database
    todo = await fetch_todo(todo_id)
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return todo

# Custom exception handler
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Database constraint violation"}
    )
```

**Key Concepts:**
- `raise HTTPException()` for expected errors
- Use `status` module for status codes
- Custom exception handlers for specific errors
- Automatic error response formatting

### 6. JWT Authentication Dependency

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

# Security scheme
security = HTTPBearer()

# JWT verification dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Verify JWT token and return current user.
    Raises 401 if token is invalid.
    """
    token = credentials.credentials
    
    try:
        # Decode JWT
        payload = jwt.decode(
            token,
            os.environ.get("BETTER_AUTH_SECRET"),
            algorithms=["HS256"]
        )
        
        # Extract user_id from token
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    # Get user from database
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    user = result.first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

# Protected endpoint
@app.get("/todos")
async def get_todos(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    # current_user is automatically provided and verified
    statement = select(Todo).where(Todo.user_id == current_user.id)
    result = await session.exec(statement)
    return result.all()
```

**Key Concepts:**
- `HTTPBearer` extracts token from Authorization header
- `Depends()` chains dependencies (get_current_user uses get_session)
- Verify JWT signature with shared secret
- Return User object for use in endpoint
- Automatic 401 response for invalid tokens

### 7. Route Organization with APIRouter

```python
from fastapi import APIRouter

# Create router
router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    dependencies=[Depends(get_current_user)]  # Apply to all routes
)

# Define routes on router
@router.get("/", response_model=List[TodoPublic])
async def get_todos(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return todos

@router.post("/", response_model=TodoPublic, status_code=201)
async def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return new_todo

# Include router in main app
app.include_router(router)
```

**Key Concepts:**
- `APIRouter` groups related endpoints
- `prefix` adds base path to all routes
- `tags` organizes docs sections
- `dependencies` applies to all routes in router
- Routes defined with `@router.method()`

## Complete CRUD Pattern

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from uuid import uuid4

router = APIRouter(prefix="/todos", tags=["todos"])

# CREATE
@router.post("/", response_model=TodoPublic, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_todo = Todo(
        id=str(uuid4()),
        **todo.dict(),
        user_id=current_user.id
    )
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo

# READ (all)
@router.get("/", response_model=List[TodoPublic])
async def get_todos(
    completed: bool | None = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(Todo.user_id == current_user.id)
    if completed is not None:
        statement = statement.where(Todo.completed == completed)
    result = await session.exec(statement)
    return result.all()

# READ (single)
@router.get("/{todo_id}", response_model=TodoPublic)
async def get_todo(
    todo_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    )
    result = await session.exec(statement)
    todo = result.first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo

# UPDATE
@router.patch("/{todo_id}", response_model=TodoPublic)
async def update_todo(
    todo_id: str,
    todo_update: TodoUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    )
    result = await session.exec(statement)
    db_todo = result.first()
    
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Update only provided fields
    update_data = todo_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo

# DELETE
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    )
    result = await session.exec(statement)
    todo = result.first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    await session.delete(todo)
    await session.commit()
    return None
```

## CORS Configuration for Production

```python
from fastapi.middleware.cors import CORSMiddleware

# Development
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Production (add deployed frontend URL)
if os.environ.get("ENVIRONMENT") == "production":
    origins.append("https://your-app.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)
```

**Key Concepts:**
- List allowed origins explicitly
- `allow_credentials=True` for cookies/auth
- Specify allowed HTTP methods
- `allow_headers=["*"]` for auth headers

## Request Validation

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: int = Field(default=3, ge=1, le=5)
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()
    
    @validator('priority')
    def priority_must_be_valid(cls, v):
        if v not in [1, 2, 3, 4, 5]:
            raise ValueError('Priority must be between 1 and 5')
        return v
```

**Key Concepts:**
- `Field()` for basic validation
- `@validator` for custom validation
- Automatic 422 response for validation errors
- Validation runs before endpoint code

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_notification(email: str, message: str):
    # Send email (example)
    print(f"Sending to {email}: {message}")

@router.post("/todos/", response_model=TodoPublic)
async def create_todo(
    todo: TodoCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    # Create todo
    db_todo = Todo(**todo.dict(), user_id=current_user.id)
    session.add(db_todo)
    await session.commit()
    
    # Queue background task
    background_tasks.add_task(
        send_notification,
        current_user.email,
        f"Todo created: {todo.title}"
    )
    
    return db_todo
```

**Key Concepts:**
- `BackgroundTasks` for async operations after response
- Don't block response for non-critical tasks
- Useful for emails, logging, cache updates

## When to Query Context7

Use the `using-context7` skill to query for:

```
✅ "FastAPI dependency injection best practices"
✅ "FastAPI async database session management"
✅ "FastAPI JWT authentication with python-jose"
✅ "FastAPI exception handlers for custom errors"
✅ "FastAPI CORS configuration for production"
✅ "FastAPI response model exclude fields"
```

Don't query for:
```
❌ HTTP status codes (200, 201, 404, 500)
❌ REST principles (GET, POST, PUT, DELETE)
❌ Python async/await syntax
❌ Basic Pydantic models
```

## Testing FastAPI Endpoints

```python
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def test_create_todo(client):
    response = client.post(
        "/todos/",
        json={"title": "Test Todo", "completed": False},
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"

@pytest.mark.asyncio
async def test_get_todos(async_client):
    response = await async_client.get(
        "/todos/",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## Common Patterns

### 1. Query Parameters with Defaults
```python
@router.get("/todos/")
async def get_todos(
    skip: int = 0,
    limit: int = 100,
    completed: bool | None = None,
    search: str | None = None
):
    # Parameters automatically extracted from URL
    pass
```

### 2. Path Parameters
```python
@router.get("/todos/{todo_id}")
async def get_todo(todo_id: str):
    # todo_id extracted from URL path
    pass
```

### 3. Request Body
```python
@router.post("/todos/")
async def create_todo(todo: TodoCreate):
    # todo parsed from JSON body
    pass
```

### 4. Headers
```python
from fastapi import Header

@router.get("/todos/")
async def get_todos(user_agent: str = Header(None)):
    # user_agent from User-Agent header
    pass
```

## Performance Tips

1. **Use async everywhere**: All I/O operations should be async
2. **Connection pooling**: Configure database pool size
3. **Response models**: Exclude unnecessary fields
4. **Caching**: Use Redis for frequently accessed data
5. **Pagination**: Always limit query results

## Integration with SQLModel

```python
# Perfect integration
@router.get("/todos/", response_model=List[TodoPublic])
async def get_todos(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(Todo.user_id == current_user.id)
    result = await session.exec(statement)
    todos = result.all()
    return todos  # Automatically serialized
```

**Key Concepts:**
- SQLModel models work directly as response_model
- Automatic serialization with `from_attributes=True`
- Type safety across database and API layers

## Related Skill Files

- `reference.md` - Quick reference for common patterns
- `examples.md` - Real Phase 2 API implementations

## Remember

- **Always use async** - `async def`, `await` for I/O
- **Type everything** - FastAPI uses types for validation
- **Dependency injection** - Clean, testable code
- **Filter by user_id** - Multi-tenant security
- **Proper status codes** - 200, 201, 204, 404, 401, 500
- **Response models** - Control what data is returned
- **Error handling** - HTTPException for expected errors
- **Query Context7** - For FastAPI-specific patterns, not HTTP basics

This skill provides the foundation for all backend API operations in Phase 2. Combine it with `sqlmodel-database` for complete CRUD implementations and `better-auth-jwt` for authentication.