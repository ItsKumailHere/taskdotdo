# SQLModel Quick Reference

## Model Definition Patterns

### Basic Table Model
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Todo(SQLModel, table=True):
    __tablename__ = "todos"  # Optional explicit name
    
    id: str = Field(primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    completed: bool = Field(default=False)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

### Field Types & Configurations

| Type | Example | Notes |
|------|---------|-------|
| `str` | `title: str` | Required string |
| `Optional[str]` | `description: Optional[str] = None` | Nullable string |
| `int` | `priority: int = 1` | Integer with default |
| `bool` | `completed: bool = False` | Boolean with default |
| `datetime` | `created_at: datetime` | Timestamp |
| `List[str]` | `tags: List[str] = []` | JSON array (PostgreSQL) |

### Field Constraints
```python
# Primary key
id: str = Field(primary_key=True)

# Foreign key
user_id: str = Field(foreign_key="users.id")

# Unique constraint
email: str = Field(unique=True)

# Index
user_id: str = Field(index=True)

# Length constraints
title: str = Field(min_length=1, max_length=200)

# Numeric constraints
priority: int = Field(ge=1, le=5)  # 1 to 5

# Default values
completed: bool = Field(default=False)
created_at: datetime = Field(default_factory=datetime.utcnow)

# Nullable (Optional)
description: Optional[str] = Field(default=None)
```

## Relationship Patterns

### One-to-Many
```python
class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str
    todos: List["Todo"] = Relationship(back_populates="user")

class Todo(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    user: Optional[User] = Relationship(back_populates="todos")
```

### Many-to-Many (Link Table)
```python
class TodoTagLink(SQLModel, table=True):
    todo_id: str = Field(foreign_key="todos.id", primary_key=True)
    tag_id: str = Field(foreign_key="tags.id", primary_key=True)

class Todo(SQLModel, table=True):
    id: str = Field(primary_key=True)
    tags: List["Tag"] = Relationship(
        back_populates="todos",
        link_model=TodoTagLink
    )

class Tag(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    todos: List[Todo] = Relationship(
        back_populates="tags",
        link_model=TodoTagLink
    )
```

## Engine & Session Setup

### Async Engine
```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# Create engine
DATABASE_URL = "postgresql+asyncpg://user:pass@host/db"
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set True for SQL logging
    pool_pre_ping=True,  # Verify connections
    pool_size=5,
    max_overflow=10
)

# Session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# FastAPI dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
```

### Neon Connection String
```python
# Format
DATABASE_URL = "postgresql+asyncpg://user:password@ep-xxx.neon.tech/dbname?sslmode=require"

# From environment
import os
DATABASE_URL = os.environ.get("DATABASE_URL")
```

## Query Patterns

### Basic CRUD

#### Create
```python
new_todo = Todo(id=str(uuid4()), title="Task", user_id="user-1")
session.add(new_todo)
await session.commit()
await session.refresh(new_todo)
```

#### Read (single)
```python
statement = select(Todo).where(Todo.id == todo_id)
result = await session.exec(statement)
todo = result.first()  # Returns None if not found
```

#### Read (multiple)
```python
statement = select(Todo).where(Todo.user_id == user_id)
result = await session.exec(statement)
todos = result.all()
```

#### Update
```python
# Get existing
statement = select(Todo).where(Todo.id == todo_id)
result = await session.exec(statement)
todo = result.first()

# Modify
todo.title = "Updated"
todo.completed = True
session.add(todo)
await session.commit()
await session.refresh(todo)
```

#### Delete
```python
statement = select(Todo).where(Todo.id == todo_id)
result = await session.exec(statement)
todo = result.first()

await session.delete(todo)
await session.commit()
```

### Filtering

#### Single condition
```python
select(Todo).where(Todo.completed == True)
select(Todo).where(Todo.user_id == user_id)
```

#### Multiple conditions (AND)
```python
select(Todo).where(
    Todo.user_id == user_id,
    Todo.completed == False
)
```

#### OR conditions
```python
from sqlalchemy import or_

select(Todo).where(
    or_(Todo.completed == True, Todo.priority == 5)
)
```

#### IN clause
```python
select(Todo).where(Todo.id.in_([id1, id2, id3]))
```

#### LIKE (partial match)
```python
select(Todo).where(Todo.title.like("%search%"))
select(Todo).where(Todo.title.ilike("%SEARCH%"))  # Case-insensitive
```

#### NULL checks
```python
select(Todo).where(Todo.description.is_(None))
select(Todo).where(Todo.description.isnot(None))
```

### Ordering
```python
# Ascending
select(Todo).order_by(Todo.created_at)

# Descending
select(Todo).order_by(Todo.created_at.desc())

# Multiple columns
select(Todo).order_by(Todo.completed, Todo.priority.desc())
```

### Pagination
```python
page = 1
page_size = 20
offset = (page - 1) * page_size

select(Todo).offset(offset).limit(page_size)
```

### Counting
```python
from sqlalchemy import func

statement = select(func.count(Todo.id)).where(Todo.user_id == user_id)
result = await session.exec(statement)
count = result.one()
```

### Aggregation
```python
from sqlalchemy import func

# Count by status
statement = select(
    Todo.completed,
    func.count(Todo.id).label("count")
).where(
    Todo.user_id == user_id
).group_by(Todo.completed)

result = await session.exec(statement)
stats = result.all()  # [(False, 5), (True, 10)]
```

## Relationship Loading

### Eager Loading (Prevent N+1)
```python
from sqlalchemy.orm import selectinload

# Load single relationship
statement = (
    select(User)
    .where(User.id == user_id)
    .options(selectinload(User.todos))
)

# Load nested relationships
statement = (
    select(User)
    .options(
        selectinload(User.todos).selectinload(Todo.tags)
    )
)
```

### Joined Loading
```python
from sqlalchemy.orm import joinedload

statement = (
    select(User)
    .where(User.id == user_id)
    .options(joinedload(User.todos))
)
```

### Lazy Loading (Default)
```python
# Without options, relationships are loaded on access
user = await session.get(User, user_id)
# Next line triggers separate query
todos = user.todos  # Lazy load
```

## Joins

### Inner Join
```python
statement = (
    select(Todo, User)
    .join(User)
    .where(User.email == "user@example.com")
)
```

### Left Outer Join
```python
from sqlalchemy import outerjoin

statement = (
    select(User, Todo)
    .outerjoin(Todo)
)
```

## Schema Operations

### Create All Tables
```python
from sqlmodel import SQLModel

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### Drop All Tables
```python
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
```

## Error Handling

### Common Exceptions
```python
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException

try:
    session.add(new_item)
    await session.commit()
except IntegrityError:
    await session.rollback()
    raise HTTPException(status_code=400, detail="Constraint violation")
except Exception as e:
    await session.rollback()
    raise HTTPException(status_code=500, detail=str(e))
```

### Transaction Management
```python
async with async_session() as session:
    try:
        session.add(item1)
        session.add(item2)
        await session.commit()
    except Exception:
        await session.rollback()
        raise
```

## Pydantic Models for API

### Request/Response Models
```python
from sqlmodel import SQLModel

# Base model (shared fields)
class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Create model (no ID, no timestamps)
class TodoCreate(TodoBase):
    pass

# Update model (all optional)
class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Public model (safe to return)
class TodoPublic(TodoBase):
    id: str
    user_id: str
    created_at: datetime

# Table model (database)
class Todo(TodoBase, table=True):
    __tablename__ = "todos"
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Performance Patterns

### Batch Operations
```python
# Batch insert
todos = [Todo(id=str(uuid4()), title=f"Task {i}") for i in range(100)]
session.add_all(todos)
await session.commit()
```

### Select Specific Columns
```python
# Instead of full model
statement = select(Todo.id, Todo.title).where(Todo.user_id == user_id)
result = await session.exec(statement)
todos = result.all()  # List of tuples
```

### Use Indexes
```python
# Add indexes to frequently queried columns
user_id: str = Field(foreign_key="users.id", index=True)
email: str = Field(unique=True, index=True)  # Unique creates index
created_at: datetime = Field(index=True)
```

## Common Gotchas

### ❌ Forgetting await
```python
# Wrong
result = session.exec(statement)  # Missing await
todos = result.all()

# Right
result = await session.exec(statement)
todos = result.all()
```

### ❌ Not committing changes
```python
# Wrong
session.add(todo)
# Changes not saved!

# Right
session.add(todo)
await session.commit()
```

### ❌ Accessing relationships without loading
```python
# N+1 problem
users = await session.exec(select(User))
for user in users:
    print(user.todos)  # Each iteration = new query!

# Right
statement = select(User).options(selectinload(User.todos))
users = await session.exec(statement)
for user in users:
    print(user.todos)  # Already loaded
```

### ❌ Not filtering by user_id (Security!)
```python
# Wrong - returns all users' todos!
statement = select(Todo).where(Todo.id == todo_id)

# Right - ensures user owns the todo
statement = select(Todo).where(
    Todo.id == todo_id,
    Todo.user_id == current_user.id
)
```

## Testing Patterns

### Test Database Setup
```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def session(test_db):
    async_session = sessionmaker(
        test_db, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
```

## Quick Command Reference

| Operation | Code |
|-----------|------|
| **Create** | `session.add(item); await session.commit()` |
| **Read One** | `await session.exec(select(Model).where(...)).first()` |
| **Read All** | `await session.exec(select(Model).where(...)).all()` |
| **Update** | `session.add(modified_item); await session.commit()` |
| **Delete** | `await session.delete(item); await session.commit()` |
| **Count** | `await session.exec(select(func.count(Model.id))).one()` |
| **Rollback** | `await session.rollback()` |
| **Refresh** | `await session.refresh(item)` |

---

This reference covers 95% of SQLModel patterns you'll need for Phase 2. For advanced patterns or Neon-specific configurations, consult the detailed skill files or use the `using-context7` skill.