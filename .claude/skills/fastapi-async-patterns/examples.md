# FastAPI Real-World Examples for Phase 2

## Example 1: Complete Backend Setup

### Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── database.py          # Database setup
│   ├── auth.py              # JWT authentication
│   ├── models.py            # SQLModel models
│   ├── schemas.py           # Pydantic request/response models
│   └── routers/
│       ├── __init__.py
│       ├── todos.py         # Todo endpoints
│       └── auth.py          # Auth endpoints
├── requirements.txt
└── .env
```

### main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import todos, auth
from app.database import init_db
import os

app = FastAPI(
    title="Todo API",
    description="Full-stack todo application with JWT authentication",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Add production origin if in production
if os.getenv("ENVIRONMENT") == "production":
    origins.append(os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(todos.router, prefix="/api")
app.include_router(auth.router, prefix="/api/auth")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Initialize database on startup
@app.on_event("startup")
async def on_startup():
    await init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### database.py
```python
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

# Initialize database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

---

## Example 2: JWT Authentication System

### auth.py (Authentication Logic)
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import get_session
from app.models import User
import os

# Security scheme
security = HTTPBearer()

# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable not set")

ALGORITHM = "HS256"

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Verify JWT token and return current user.
    
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    token = credentials.credentials
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    user = result.first()
    
    if user is None:
        raise credentials_exception
    
    return user

# Optional: Dependency for optional authentication
async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User | None:
    """
    Same as get_current_user but returns None if authentication fails.
    Useful for endpoints that work with or without auth.
    """
    try:
        return await get_current_user(credentials, session)
    except HTTPException:
        return None
```

### routers/auth.py (Auth Endpoints)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.database import get_session
from app.models import User
from app.schemas import UserPublic

router = APIRouter(tags=["authentication"])

@router.get("/me", response_model=UserPublic)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information."""
    return current_user

@router.get("/verify")
async def verify_token(
    current_user: User = Depends(get_current_user)
):
    """Verify if token is valid."""
    return {"valid": True, "user_id": current_user.id}
```

---

## Example 3: Complete Todo CRUD Router

### routers/todos.py
```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from uuid import uuid4
from datetime import datetime, timezone

from app.database import get_session
from app.auth import get_current_user
from app.models import Todo, User
from app.schemas import TodoCreate, TodoUpdate, TodoPublic

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    dependencies=[Depends(get_current_user)]  # All routes require auth
)

@router.post("/", response_model=TodoPublic, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new todo.
    
    - **title**: Todo title (required, 1-200 characters)
    - **description**: Optional description
    - **completed**: Initial completion status (default: false)
    """
    db_todo = Todo(
        id=str(uuid4()),
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=current_user.id,
        created_at=datetime.now(timezone.utc)
    )
    
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    
    return db_todo

@router.get("/", response_model=List[TodoPublic])
async def get_todos(
    completed: bool | None = Query(None, description="Filter by completion status"),
    search: str | None = Query(None, description="Search in title and description"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max records to return"),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all todos for the authenticated user.
    
    Supports filtering, search, and pagination.
    """
    # Base query - always filter by user_id
    statement = select(Todo).where(Todo.user_id == current_user.id)
    
    # Apply filters
    if completed is not None:
        statement = statement.where(Todo.completed == completed)
    
    if search:
        search_pattern = f"%{search}%"
        statement = statement.where(
            or_(
                Todo.title.ilike(search_pattern),
                Todo.description.ilike(search_pattern)
            )
        )
    
    # Pagination and ordering
    statement = (
        statement
        .order_by(Todo.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    
    result = await session.exec(statement)
    return result.all()

@router.get("/stats")
async def get_todo_stats(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get statistics about user's todos."""
    from sqlalchemy import func
    
    # Total count
    total_stmt = select(func.count(Todo.id)).where(
        Todo.user_id == current_user.id
    )
    total_result = await session.exec(total_stmt)
    total = total_result.one()
    
    # Completed count
    completed_stmt = select(func.count(Todo.id)).where(
        Todo.user_id == current_user.id,
        Todo.completed == True
    )
    completed_result = await session.exec(completed_stmt)
    completed = completed_result.one()
    
    pending = total - completed
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": round(completion_rate, 2)
    }

@router.get("/{todo_id}", response_model=TodoPublic)
async def get_todo(
    todo_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific todo by ID."""
    statement = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    )
    result = await session.exec(statement)
    todo = result.first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    return todo

@router.patch("/{todo_id}", response_model=TodoPublic)
async def update_todo(
    todo_id: str,
    todo_update: TodoUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update a todo. Only provided fields are updated.
    """
    # Get existing todo
    statement = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    )
    result = await session.exec(statement)
    db_todo = result.first()
    
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    # Update only provided fields
    update_data = todo_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    # Update timestamp
    db_todo.updated_at = datetime.now(timezone.utc)
    
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    
    return db_todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a todo."""
    statement = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    )
    result = await session.exec(statement)
    todo = result.first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    await session.delete(todo)
    await session.commit()
    
    return None

@router.patch("/complete-all", response_model=dict)
async def complete_all_todos(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Mark all incomplete todos as completed."""
    statement = select(Todo).where(
        Todo.user_id == current_user.id,
        Todo.completed == False
    )
    result = await session.exec(statement)
    todos = result.all()
    
    for todo in todos:
        todo.completed = True
        todo.updated_at = datetime.now(timezone.utc)
        session.add(todo)
    
    await session.commit()
    
    return {"updated": len(todos), "message": f"Marked {len(todos)} todos as completed"}
```

---

## Example 4: Pydantic Request/Response Models

### schemas.py
```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

# ==================== Todo Models ====================

class TodoBase(BaseModel):
    """Base todo fields shared across models."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False

class TodoCreate(TodoBase):
    """Model for creating a todo."""
    
    @validator('title')
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or just whitespace')
        return v.strip()

class TodoUpdate(BaseModel):
    """Model for updating a todo. All fields optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    
    @validator('title')
    def title_not_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty or just whitespace')
        return v.strip() if v else v

class TodoPublic(TodoBase):
    """Model for returning todo data. Includes all fields safe to expose."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel

# ==================== User Models ====================

class UserBase(BaseModel):
    """Base user fields."""
    email: str = Field(..., max_length=255)
    name: str = Field(..., min_length=1, max_length=100)

class UserPublic(UserBase):
    """Public user model (safe to expose)."""
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== Response Models ====================

class MessageResponse(BaseModel):
    """Generic message response."""
    message: str

class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str

class StatsResponse(BaseModel):
    """Todo statistics response."""
    total: int
    completed: int
    pending: int
    completion_rate: float
```

---

## Example 5: Advanced Error Handling

### Custom Exception Handlers

```python
# In main.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors (unique constraints, foreign keys)."""
    error_msg = str(exc.orig)
    
    if "unique constraint" in error_msg.lower():
        detail = "A record with this value already exists"
    elif "foreign key" in error_msg.lower():
        detail = "Referenced record does not exist"
    else:
        detail = "Database constraint violation"
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": detail}
    )

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception):
    """Catch-all handler for unexpected errors."""
    # Log the error
    print(f"Unexpected error: {exc}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"}
    )
```

---

## Example 6: Background Tasks

### Email Notifications

```python
from fastapi import BackgroundTasks

def send_notification_email(email: str, message: str):
    """Simulate sending email (replace with actual email service)."""
    print(f"Sending email to {email}: {message}")
    # In production: use SendGrid, AWS SES, etc.

@router.post("/", response_model=TodoPublic, status_code=201)
async def create_todo_with_notification(
    todo: TodoCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create todo and send notification in background."""
    # Create todo
    db_todo = Todo(
        id=str(uuid4()),
        **todo.dict(),
        user_id=current_user.id
    )
    
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    
    # Queue background task
    background_tasks.add_task(
        send_notification_email,
        current_user.email,
        f"New todo created: {todo.title}"
    )
    
    return db_todo
```

---

## Example 7: Testing

### test_todos.py

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from app.main import app
from app.database import get_session

# Test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
def client(test_engine):
    def override_get_session():
        # Provide test session
        pass
    
    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)

def test_create_todo(client):
    """Test creating a todo."""
    response = client.post(
        "/api/todos/",
        json={
            "title": "Test Todo",
            "description": "Test description",
            "completed": False
        },
        headers={"Authorization": "Bearer test-token"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["completed"] == False
    assert "id" in data

def test_get_todos(client):
    """Test getting all todos."""
    response = client.get(
        "/api/todos/",
        headers={"Authorization": "Bearer test-token"}
    )
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_todo_not_found(client):
    """Test getting non-existent todo."""
    response = client.get(
        "/api/todos/nonexistent-id",
        headers={"Authorization": "Bearer test-token"}
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_unauthorized_access(client):
    """Test accessing protected route without auth."""
    response = client.get("/api/todos/")
    assert response.status_code == 401
```

---

## Example 8: Environment Configuration

### config.py

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str
    
    # Authentication
    better_auth_secret: str
    
    # Application
    environment: str = "development"
    debug: bool = False
    
    # CORS
    frontend_url: str = "http://localhost:3000"
    
    # API
    api_prefix: str = "/api"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Usage in app
settings = get_settings()
```

---

## Key Takeaways from Examples

1. **Async everywhere** - All endpoints and database operations use async/await
2. **Dependency injection** - Session and auth injected cleanly
3. **Type safety** - Full type hints for validation and documentation
4. **User isolation** - Always filter by `user_id` for security
5. **Proper status codes** - 201 for create, 204 for delete, 404 for not found
6. **Error handling** - HTTPException for expected errors, custom handlers for unexpected
7. **Response models** - Control what data is exposed
8. **Router organization** - Group related endpoints with APIRouter
9. **Background tasks** - Non-blocking operations after response
10. **Testing** - TestClient for synchronous, AsyncClient for async tests

These examples cover all FastAPI patterns needed for Phase 2!