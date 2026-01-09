# Database Module

This module provides the database infrastructure for the Multi-User Todo Application using SQLModel with async support.

## Components

### 1. Database Engines (`database.py`)
- **Sync Engine**: Standard SQLAlchemy engine for synchronous operations
- **Async Engine**: Async SQLAlchemy engine with asyncpg for asynchronous operations
- **Neon PostgreSQL Optimized**: Configured with appropriate connection pooling for Neon

### 2. Session Management (`session.py`)
- **AsyncSessionLocal**: Async session factory
- **SyncSessionLocal**: Sync session factory  
- **get_async_session()**: Async context manager for database sessions
- **get_sync_session()**: Sync context manager for database sessions
- **get_db_session()**: FastAPI dependency for injecting async database sessions

### 3. Migrations (`migrations.py`)
- **Alembic Integration**: Properly configured for SQLModel
- **Programmatic Migration Execution**: Functions to run migrations programmatically
- **Autogenerate Support**: Automatic migration generation from model changes

## Configuration

The database is configured through environment variables in `app/config/settings.py`:
- `DATABASE_URL`: PostgreSQL connection string
- Neon-specific configurations are automatically applied

## Usage

### In FastAPI Routes
```python
from fastapi import Depends
from app.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

@app.get("/todos")
async def get_todos(
    db: AsyncSession = Depends(get_db_session)
):
    # Use db for database operations
    pass
```

### Standalone Usage
```python
from app.database import get_async_session

async def some_function():
    async with get_async_session() as session:
        # Use session for database operations
        pass
```

## Neon PostgreSQL Specifics

- Connection pooling optimized for serverless environments
- Appropriate timeout settings for Neon's connection behavior
- Application name set for better monitoring in Neon dashboard