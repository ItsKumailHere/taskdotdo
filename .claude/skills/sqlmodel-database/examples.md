# SQLModel Real-World Examples for Phase 2

## Example 1: Complete Todo App Database Setup

### Models with Relationships

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
from uuid import uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))
    email: str = Field(unique=True, index=True)
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    todos: List["Todo"] = Relationship(back_populates="user")

class Todo(SQLModel, table=True):
    __tablename__ = "todos"
    
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: int = Field(default=3, ge=1, le=5)
    due_date: Optional[datetime] = Field(default=None)
    
    # Foreign key
    user_id: str = Field(foreign_key="users.id", index=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="todos")
```

### Database Configuration

```python
# backend/app/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Get Neon database URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set True for development SQL logging
    pool_pre_ping=True,  # Verify connections before use
    pool_size=5,  # Limit connections for Neon
    max_overflow=10
)

# Create session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False  # Prevent lazy loading issues
)

# Dependency for FastAPI
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Initialize database (create tables)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

---

## Example 2: CRUD Operations with User Isolation

### Create Todo (Filtered by User)

```python
from fastapi import Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import uuid4

@app.post("/todos", response_model=TodoPublic, status_code=201)
async def create_todo(
    todo: TodoCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new todo for the authenticated user."""
    
    # Create todo instance
    db_todo = Todo(
        id=str(uuid4()),
        title=todo.title,
        description=todo.description,
        completed=False,
        user_id=current_user.id,  # Always use authenticated user
        created_at=datetime.now(timezone.utc)
    )
    
    # Save to database
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    
    return db_todo
```

### Get All Todos (User-Specific)

```python
from sqlmodel import select

@app.get("/todos", response_model=List[TodoPublic])
async def get_todos(
    completed: Optional[bool] = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all todos for authenticated user, optionally filtered by completed status."""
    
    # Base query - always filter by user_id
    statement = select(Todo).where(Todo.user_id == current_user.id)
    
    # Optional filtering
    if completed is not None:
        statement = statement.where(Todo.completed == completed)
    
    # Order by created_at desc
    statement = statement.order_by(Todo.created_at.desc())
    
    # Execute
    result = await session.exec(statement)
    return result.all()
```

### Get Single Todo (With Ownership Check)

```python
@app.get("/todos/{todo_id}", response_model=TodoPublic)
async def get_todo(
    todo_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific todo by ID."""
    
    # Query with user_id check for security
    statement = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == current_user.id  # Ensure user owns this todo
    )
    
    result = await session.exec(statement)
    todo = result.first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo
```

### Update Todo (Partial Update)

```python
@app.patch("/todos/{todo_id}", response_model=TodoPublic)
async def update_todo(
    todo_id: str,
    todo_update: TodoUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a todo. Only provided fields are updated."""
    
    # Get existing todo with ownership check
    statement = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    )
    result = await session.exec(statement)
    db_todo = result.first()
    
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update only provided fields
    update_data = todo_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    # Update timestamp
    db_todo.updated_at = datetime.now(timezone.utc)
    
    # Save changes
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    
    return db_todo
```

### Delete Todo

```python
@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a todo."""
    
    # Get todo with ownership check
    statement = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    )
    result = await session.exec(statement)
    todo = result.first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Delete
    await session.delete(todo)
    await session.commit()
    
    return None  # 204 No Content
```

---

## Example 3: Advanced Queries

### Get Todo Statistics

```python
from sqlalchemy import func

@app.get("/todos/stats")
async def get_todo_stats(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get statistics about user's todos."""
    
    # Total count
    total_statement = select(func.count(Todo.id)).where(
        Todo.user_id == current_user.id
    )
    total_result = await session.exec(total_statement)
    total = total_result.one()
    
    # Completed count
    completed_statement = select(func.count(Todo.id)).where(
        Todo.user_id == current_user.id,
        Todo.completed == True
    )
    completed_result = await session.exec(completed_statement)
    completed = completed_result.one()
    
    # Pending count
    pending = total - completed
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": (completed / total * 100) if total > 0 else 0
    }
```

### Search Todos

```python
@app.get("/todos/search", response_model=List[TodoPublic])
async def search_todos(
    q: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Search todos by title or description."""
    
    search_pattern = f"%{q}%"
    
    statement = select(Todo).where(
        Todo.user_id == current_user.id,
        or_(
            Todo.title.ilike(search_pattern),
            Todo.description.ilike(search_pattern)
        )
    ).order_by(Todo.created_at.desc())
    
    result = await session.exec(statement)
    return result.all()
```

### Paginated Todos

```python
@app.get("/todos/paginated", response_model=dict)
async def get_todos_paginated(
    page: int = 1,
    page_size: int = 20,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get paginated todos."""
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Get total count
    count_statement = select(func.count(Todo.id)).where(
        Todo.user_id == current_user.id
    )
    count_result = await session.exec(count_statement)
    total = count_result.one()
    
    # Get paginated results
    statement = (
        select(Todo)
        .where(Todo.user_id == current_user.id)
        .order_by(Todo.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    
    result = await session.exec(statement)
    todos = result.all()
    
    return {
        "todos": todos,
        "page": page,
        "page_size": page_size,
        "total": total,
        "pages": (total + page_size - 1) // page_size  # Ceiling division
    }
```

---

## Example 4: Relationship Loading

### Get User with All Todos (Eager Loading)

```python
from sqlalchemy.orm import selectinload

@app.get("/users/me/profile")
async def get_user_profile(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get user profile with all todos."""
    
    # Eager load todos to prevent N+1 queries
    statement = (
        select(User)
        .where(User.id == current_user.id)
        .options(selectinload(User.todos))
    )
    
    result = await session.exec(statement)
    user = result.first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Access todos without additional query
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "todos_count": len(user.todos),
        "completed_count": len([t for t in user.todos if t.completed])
    }
```

### Avoid N+1 Query Problem

```python
# ❌ Bad - N+1 queries (one for users, N for each user's todos)
async def bad_example(session: AsyncSession):
    statement = select(User)
    result = await session.exec(statement)
    users = result.all()
    
    for user in users:
        print(user.todos)  # Triggers separate query for each user!

# ✅ Good - Single additional query for all todos
async def good_example(session: AsyncSession):
    statement = select(User).options(selectinload(User.todos))
    result = await session.exec(statement)
    users = result.all()
    
    for user in users:
        print(user.todos)  # No additional query!
```

---

## Example 5: Error Handling

### Handling Constraint Violations

```python
from sqlalchemy.exc import IntegrityError

@app.post("/todos", response_model=TodoPublic, status_code=201)
async def create_todo_with_error_handling(
    todo: TodoCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create todo with proper error handling."""
    
    db_todo = Todo(
        id=str(uuid4()),
        title=todo.title,
        user_id=current_user.id
    )
    
    try:
        session.add(db_todo)
        await session.commit()
        await session.refresh(db_todo)
        return db_todo
        
    except IntegrityError as e:
        await session.rollback()
        
        # Check specific constraint
        if "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail="A todo with this title already exists"
            )
        elif "foreign key" in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail="Invalid user reference"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Database constraint violation"
            )
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create todo: {str(e)}"
        )
```

---

## Example 6: Bulk Operations

### Bulk Insert Todos

```python
@app.post("/todos/bulk", response_model=List[TodoPublic])
async def create_bulk_todos(
    todos: List[TodoCreate],
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create multiple todos at once."""
    
    # Create todo instances
    db_todos = [
        Todo(
            id=str(uuid4()),
            title=todo.title,
            description=todo.description,
            user_id=current_user.id,
            created_at=datetime.now(timezone.utc)
        )
        for todo in todos
    ]
    
    # Bulk add
    session.add_all(db_todos)
    await session.commit()
    
    # Refresh all
    for todo in db_todos:
        await session.refresh(todo)
    
    return db_todos
```

### Bulk Update (Mark All Complete)

```python
@app.patch("/todos/complete-all", response_model=dict)
async def complete_all_todos(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Mark all user's todos as completed."""
    
    # Get all incomplete todos
    statement = select(Todo).where(
        Todo.user_id == current_user.id,
        Todo.completed == False
    )
    result = await session.exec(statement)
    todos = result.all()
    
    # Update all
    for todo in todos:
        todo.completed = True
        todo.updated_at = datetime.now(timezone.utc)
        session.add(todo)
    
    await session.commit()
    
    return {"updated": len(todos)}
```

---

## Example 7: Complex Filtering

### Filter by Multiple Criteria

```python
@app.get("/todos/filter", response_model=List[TodoPublic])
async def filter_todos(
    completed: Optional[bool] = None,
    priority: Optional[int] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Filter todos with multiple criteria."""
    
    # Start with base query
    statement = select(Todo).where(Todo.user_id == current_user.id)
    
    # Apply filters
    if completed is not None:
        statement = statement.where(Todo.completed == completed)
    
    if priority is not None:
        statement = statement.where(Todo.priority == priority)
    
    if search:
        search_pattern = f"%{search}%"
        statement = statement.where(
            or_(
                Todo.title.ilike(search_pattern),
                Todo.description.ilike(search_pattern)
            )
        )
    
    # Apply sorting
    sort_column = getattr(Todo, sort_by, Todo.created_at)
    if sort_order == "desc":
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column)
    
    # Execute
    result = await session.exec(statement)
    return result.all()
```

---

## Example 8: Transaction Management

### Create Todo with Associated Data

```python
@app.post("/todos/with-tags", response_model=TodoPublic)
async def create_todo_with_tags(
    todo: TodoCreate,
    tag_names: List[str],
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a todo with associated tags in a transaction."""
    
    try:
        # Create todo
        db_todo = Todo(
            id=str(uuid4()),
            title=todo.title,
            user_id=current_user.id
        )
        session.add(db_todo)
        
        # Create or get tags
        for tag_name in tag_names:
            # Check if tag exists
            tag_statement = select(Tag).where(Tag.name == tag_name)
            tag_result = await session.exec(tag_statement)
            tag = tag_result.first()
            
            if not tag:
                # Create new tag
                tag = Tag(id=str(uuid4()), name=tag_name)
                session.add(tag)
            
            # Associate tag with todo
            db_todo.tags.append(tag)
        
        # Commit everything together
        await session.commit()
        await session.refresh(db_todo)
        
        return db_todo
        
    except Exception as e:
        # Rollback if anything fails
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create todo with tags: {str(e)}"
        )
```

---

## Example 9: Testing Patterns

### Test Database Setup

```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

@pytest.fixture
async def test_engine():
    """Create in-memory SQLite database for testing."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=True
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield engine
    
    # Cleanup
    await engine.dispose()

@pytest.fixture
async def test_session(test_engine):
    """Provide test database session."""
    async_session = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session

@pytest.mark.asyncio
async def test_create_todo(test_session):
    """Test creating a todo."""
    # Create user
    user = User(id="test-user", email="test@example.com", name="Test")
    test_session.add(user)
    await test_session.commit()
    
    # Create todo
    todo = Todo(
        id="test-todo",
        title="Test Task",
        user_id=user.id
    )
    test_session.add(todo)
    await test_session.commit()
    
    # Verify
    statement = select(Todo).where(Todo.id == "test-todo")
    result = await test_session.exec(statement)
    saved_todo = result.first()
    
    assert saved_todo is not None
    assert saved_todo.title == "Test Task"
    assert saved_todo.user_id == user.id
```

---

## Key Takeaways from Examples

1. **Always filter by `user_id`** for multi-tenant security
2. **Use `await` for all async operations** (exec, commit, refresh, delete)
3. **Handle errors properly** with rollback on exceptions
4. **Eager load relationships** to prevent N+1 queries
5. **Use proper HTTP status codes** (201 for create, 204 for delete, 404 for not found)
6. **Validate ownership** before update/delete operations
7. **Use transactions** for operations involving multiple models
8. **Return appropriate Pydantic models** (TodoPublic, not internal Todo)

These examples cover 90% of database operations you'll need in Phase 2!