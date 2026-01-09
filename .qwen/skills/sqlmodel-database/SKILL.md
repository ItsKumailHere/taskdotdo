---
name: sqlmodel-database
description: Expert in SQLModel ORM patterns for async PostgreSQL operations. Covers model definitions, relationships, async session management, queries with filtering/joins, and Neon PostgreSQL integration. Use for all database schema and query implementations.
---

# SQLModel Database - Async PostgreSQL with Neon

You are an expert in SQLModel, the Python library that combines SQLAlchemy and Pydantic for type-safe database operations. This skill covers async patterns for PostgreSQL, specifically with Neon Serverless PostgreSQL.

## Core Philosophy

**SQLModel = Pydantic Models + SQLAlchemy ORM**

- **Type safety**: Full Python type hints and validation
- **Async-first**: All operations use `async`/`await`
- **Pydantic integration**: Automatic validation and serialization
- **SQLAlchemy foundation**: Powerful query capabilities
- **Neon optimized**: Connection pooling for serverless environments

## When to Use This Skill

✅ **Use this skill for:**
- Defining database models with proper types and constraints
- Creating table relationships (one-to-many, many-to-many)
- Writing async database queries with filtering and joins
- Managing async database sessions
- Setting up Neon PostgreSQL connections
- Handling migrations and schema changes
- Optimizing queries with relationship loading

❌ **Don't use for:**
- Basic SQL syntax (SELECT, WHERE) - you know this
- General database concepts - fundamental knowledge
- Python async/await basics - covered in training

## Fundamental Patterns

### 1. Model Definition

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Todo(SQLModel, table=True):
    __tablename__ = "todos"  # Optional: explicit table name
    
    # Primary key
    id: str = Field(primary_key=True)
    
    # Required fields
    title: str = Field(index=True)  # Add index for frequent queries
    user_id: str = Field(foreign_key="users.id", index=True)
    
    # Optional fields with defaults
    completed: bool = Field(default=False)
    description: Optional[str] = Field(default=None)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)
```

**Key Concepts:**
- `table=True` marks this as a database table
- `Field()` provides database-specific configuration
- Type hints are required and enforced
- Optional fields use `Optional[Type]` or `Type | None`
- Foreign keys reference "table.column"

### 2. Async Session Management

```python
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# Create async engine
DATABASE_URL = "postgresql+asyncpg://user:pass@host/db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create async session factory
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Dependency for FastAPI
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
```

**Key Concepts:**
- Use `asyncpg` driver for PostgreSQL (`postgresql+asyncpg://`)
- `expire_on_commit=False` prevents lazy loading issues
- Always use context managers (`async with`)
- Yield session in FastAPI dependencies

### 3. Basic Queries

```python
from sqlmodel import select

# SELECT with filtering
async def get_user_todos(session: AsyncSession, user_id: str):
    statement = select(Todo).where(Todo.user_id == user_id)
    result = await session.exec(statement)
    return result.all()

# SELECT single record
async def get_todo_by_id(session: AsyncSession, todo_id: str):
    statement = select(Todo).where(Todo.id == todo_id)
    result = await session.exec(statement)
    return result.first()  # Returns None if not found

# INSERT
async def create_todo(session: AsyncSession, todo: Todo):
    session.add(todo)
    await session.commit()
    await session.refresh(todo)  # Get DB-generated values
    return todo

# UPDATE
async def update_todo(session: AsyncSession, todo: Todo):
    session.add(todo)  # Works for updates too
    await session.commit()
    await session.refresh(todo)
    return todo

# DELETE
async def delete_todo(session: AsyncSession, todo: Todo):
    await session.delete(todo)
    await session.commit()
```

**Key Concepts:**
- Build queries with `select(Model).where(...)`
- Execute with `await session.exec(statement)`
- `.all()` returns list, `.first()` returns single/None
- Always `await session.commit()` after changes
- `await session.refresh()` to get updated values

### 4. Relationships

```python
from sqlmodel import Relationship
from typing import List

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    
    # One-to-many: one user has many todos
    todos: List["Todo"] = Relationship(back_populates="user")

class Todo(SQLModel, table=True):
    __tablename__ = "todos"
    
    id: str = Field(primary_key=True)
    title: str
    user_id: str = Field(foreign_key="users.id")
    
    # Many-to-one: many todos belong to one user
    user: Optional[User] = Relationship(back_populates="todos")
```

**Key Concepts:**
- `Relationship()` defines ORM relationships (not database constraints)
- `back_populates` must match field name on other model
- Forward reference with quotes: `List["Todo"]`
- Foreign key defined separately with `Field(foreign_key=...)`

### 5. Relationship Loading

```python
from sqlalchemy.orm import selectinload

# Eager load relationships (prevents N+1 queries)
async def get_user_with_todos(session: AsyncSession, user_id: str):
    statement = (
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.todos))  # Load todos eagerly
    )
    result = await session.exec(statement)
    return result.first()

# Access loaded relationships
user = await get_user_with_todos(session, "user-123")
for todo in user.todos:  # No additional query needed
    print(todo.title)
```

**Key Concepts:**
- `selectinload()` loads relationships in single query
- Prevents N+1 query problem
- Use for relationships you know you'll access
- Alternative: `joinedload()` for left joins

## Integration with FastAPI

```python
from fastapi import Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

@app.post("/todos", response_model=TodoPublic)
async def create_todo(
    todo: TodoCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Create model instance
    db_todo = Todo(
        id=str(uuid4()),
        title=todo.title,
        user_id=current_user.id,
        completed=False
    )
    
    # Save to database
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    
    return db_todo

@app.get("/todos", response_model=List[TodoPublic])
async def get_todos(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(Todo.user_id == current_user.id)
    result = await session.exec(statement)
    return result.all()
```

**Key Concepts:**
- Inject `AsyncSession` via `Depends(get_session)`
- Always filter by `user_id` for multi-tenant security
- Use Pydantic models for request/response (TodoCreate, TodoPublic)
- SQLModel instances can be returned directly (auto-serialization)

## Neon PostgreSQL Specifics

### Connection String Format
```python
# Neon connection string
DATABASE_URL = "postgresql+asyncpg://user:password@host.neon.tech/dbname?sslmode=require"

# From environment
import os
DATABASE_URL = os.environ.get("DATABASE_URL")

# Engine configuration for Neon
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set True for SQL logging
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,  # Limit connection pool
    max_overflow=10
)
```

**Neon Considerations:**
- Always use SSL: `?sslmode=require`
- Connection pooling limits for serverless
- Use `pool_pre_ping=True` to handle stale connections
- Neon auto-scales, but respect connection limits

## Schema Creation

```python
from sqlmodel import SQLModel

# Create all tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Drop all tables (development only!)
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
```

**Key Concepts:**
- `create_all()` creates tables if they don't exist
- Use for initial setup or simple projects
- For production, use Alembic migrations (see migrations.md)

## Common Query Patterns

### Filtering
```python
# Multiple conditions
statement = select(Todo).where(
    Todo.user_id == user_id,
    Todo.completed == False
)

# OR conditions
from sqlalchemy import or_
statement = select(Todo).where(
    or_(Todo.completed == True, Todo.user_id == user_id)
)

# LIKE for partial matching
statement = select(Todo).where(Todo.title.like("%search%"))
```

### Ordering
```python
statement = select(Todo).order_by(Todo.created_at.desc())
statement = select(Todo).order_by(Todo.completed, Todo.title)
```

### Pagination
```python
page = 1
page_size = 20
offset = (page - 1) * page_size

statement = (
    select(Todo)
    .where(Todo.user_id == user_id)
    .offset(offset)
    .limit(page_size)
)
```

### Counting
```python
from sqlalchemy import func

statement = select(func.count(Todo.id)).where(Todo.user_id == user_id)
result = await session.exec(statement)
count = result.one()
```

## When to Query Context7

Use the `using-context7` skill to query for:

```
✅ "SQLModel async session management best practices"
✅ "SQLModel relationship loading with selectinload"
✅ "SQLModel Alembic migrations setup"
✅ "Neon PostgreSQL connection string format for SQLModel"
✅ "SQLModel with FastAPI dependency injection patterns"
```

Don't query for:
```
❌ Basic SQL syntax (SELECT, WHERE, JOIN)
❌ Python type hints
❌ General database concepts
❌ Python async/await basics
```

## Error Handling

```python
from sqlalchemy.exc import IntegrityError, NoResultFound

try:
    session.add(new_todo)
    await session.commit()
except IntegrityError as e:
    await session.rollback()
    raise HTTPException(status_code=400, detail="Duplicate or invalid data")
except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))
```

**Key Concepts:**
- Always `await session.rollback()` on errors
- `IntegrityError` for constraint violations (unique, foreign key)
- Handle in FastAPI with appropriate HTTP status codes

## Performance Tips

1. **Use indexes** on frequently queried columns:
   ```python
   user_id: str = Field(foreign_key="users.id", index=True)
   ```

2. **Eager load relationships** to prevent N+1:
   ```python
   .options(selectinload(User.todos))
   ```

3. **Select specific columns** when not needing full objects:
   ```python
   statement = select(Todo.id, Todo.title).where(...)
   ```

4. **Use pagination** for large result sets:
   ```python
   .offset(offset).limit(limit)
   ```

5. **Connection pooling** for Neon:
   ```python
   engine = create_async_engine(url, pool_size=5, max_overflow=10)
   ```

## Related Skill Files

- `model-patterns.md` - Model definitions and Field configurations
- `query-patterns.md` - Advanced queries, joins, aggregations
- `session-management.md` - Session lifecycle and context managers
- `neon-specific.md` - Neon PostgreSQL connection and pooling
- `migrations.md` - Alembic setup and schema migrations
- `reference.md` - Quick reference for common patterns
- `examples.md` - Real Phase 2 database scenarios

## Remember

- **Always use async** - `async def`, `await session.exec()`, `await session.commit()`
- **Type everything** - SQLModel enforces types for safety
- **Filter by user_id** - Multi-tenant security is critical
- **Use relationships wisely** - Eager load to prevent N+1 queries
- **Handle errors** - Rollback on exceptions, return proper HTTP codes
- **Query Context7** - For framework-specific patterns, not SQL basics

This skill provides the foundation for all database operations in Phase 2. Combine it with `fastapi-async-patterns` for complete CRUD implementations.
