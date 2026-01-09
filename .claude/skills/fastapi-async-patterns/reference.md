# FastAPI Quick Reference

## Application Setup

### Basic App
```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### With CORS
```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## HTTP Methods

| Method | Decorator | Use Case |
|--------|-----------|----------|
| GET | `@app.get()` | Read/retrieve data |
| POST | `@app.post()` | Create new resource |
| PUT | `@app.put()` | Replace entire resource |
| PATCH | `@app.patch()` | Partial update |
| DELETE | `@app.delete()` | Delete resource |

## Status Codes

```python
from fastapi import status

# Success
status.HTTP_200_OK              # Default for GET
status.HTTP_201_CREATED         # Resource created
status.HTTP_204_NO_CONTENT      # Success, no content (DELETE)

# Client Errors
status.HTTP_400_BAD_REQUEST     # Invalid request
status.HTTP_401_UNAUTHORIZED    # Authentication required
status.HTTP_403_FORBIDDEN       # Authenticated but no permission
status.HTTP_404_NOT_FOUND       # Resource not found
status.HTTP_422_UNPROCESSABLE_ENTITY  # Validation error

# Server Errors
status.HTTP_500_INTERNAL_SERVER_ERROR
```

## Endpoint Patterns

### Path Parameters
```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}
```

### Query Parameters
```python
@app.get("/items/")
async def list_items(
    skip: int = 0,
    limit: int = 10,
    search: str | None = None
):
    return {"skip": skip, "limit": limit, "search": search}
```

### Request Body
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Headers
```python
from fastapi import Header

@app.get("/items/")
async def get_items(user_agent: str | None = Header(None)):
    return {"User-Agent": user_agent}
```

### Cookies
```python
from fastapi import Cookie

@app.get("/items/")
async def get_items(session_id: str | None = Cookie(None)):
    return {"session_id": session_id}
```

## Dependency Injection

### Basic Dependency
```python
from fastapi import Depends

def common_parameters(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

### Async Dependency
```python
async def get_db():
    db = Database()
    try:
        yield db
    finally:
        await db.close()

@app.get("/items/")
async def read_items(db = Depends(get_db)):
    return await db.get_items()
```

### Class-Based Dependency
```python
class DatabaseSession:
    def __init__(self):
        self.session = create_session()
    
    async def __call__(self):
        try:
            yield self.session
        finally:
            await self.session.close()

get_db = DatabaseSession()

@app.get("/items/")
async def read_items(session = Depends(get_db)):
    return session.query(...)
```

### Dependency Chain
```python
def get_token(token: str = Header(...)):
    return token

def verify_token(token: str = Depends(get_token)):
    # Verify logic
    return user_id

@app.get("/profile")
async def get_profile(user_id: str = Depends(verify_token)):
    return {"user_id": user_id}
```

## Pydantic Models

### Basic Model
```python
from pydantic import BaseModel, Field
from typing import Optional

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False
```

### With Validators
```python
from pydantic import validator

class TodoCreate(BaseModel):
    title: str
    priority: int
    
    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @validator('priority')
    def priority_in_range(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Priority must be 1-5')
        return v
```

### Config
```python
class TodoPublic(BaseModel):
    id: str
    title: str
    
    class Config:
        from_attributes = True  # Enable ORM mode (SQLModel)
```

## Response Models

### Specify Response Model
```python
@app.get("/todos/{todo_id}", response_model=TodoPublic)
async def get_todo(todo_id: str):
    return db_todo  # Automatically serialized
```

### List Response
```python
from typing import List

@app.get("/todos/", response_model=List[TodoPublic])
async def get_todos():
    return todos
```

### Exclude Fields
```python
@app.get("/todos/", response_model=TodoPublic, response_model_exclude={"internal_field"})
async def get_todos():
    return todos
```

### Status Code
```python
@app.post("/todos/", response_model=TodoPublic, status_code=201)
async def create_todo(todo: TodoCreate):
    return new_todo
```

## Error Handling

### HTTPException
```python
from fastapi import HTTPException, status

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return database[item_id]
```

### Custom Exception Handler
```python
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message}
    )
```

### Validation Error Handler
```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

## APIRouter

### Create Router
```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def get_todos():
    return todos

@router.post("/")
async def create_todo(todo: TodoCreate):
    return new_todo
```

### Include Router
```python
app.include_router(router)

# With prefix
app.include_router(router, prefix="/api/v1")

# With tags
app.include_router(router, tags=["v1"])
```

## Security

### HTTPBearer
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

security = HTTPBearer()

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return credentials.credentials

@app.get("/protected")
async def protected_route(token: str = Depends(get_token)):
    return {"token": token}
```

### JWT Authentication
```python
from jose import jwt, JWTError

def verify_token(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/profile")
async def get_profile(user_id: str = Depends(verify_token)):
    return {"user_id": user_id}
```

## Background Tasks

### Simple Background Task
```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_log, f"Email sent to {email}")
    return {"message": "Email sent"}
```

### With Parameters
```python
def send_email(email: str, message: str):
    print(f"Sending to {email}: {message}")

@app.post("/notify/")
async def notify(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Hello!")
    return {"status": "sent"}
```

## File Uploads

### Single File
```python
from fastapi import File, UploadFile

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

### Multiple Files
```python
from typing import List

@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile] = File(...)):
    return {"filenames": [f.filename for f in files]}
```

## Middleware

### Custom Middleware
```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Database Integration (SQLModel)

### Setup
```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@host/db"

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with async_session() as session:
        yield session
```

### CRUD Endpoint
```python
from sqlmodel import select

@app.get("/todos/", response_model=List[TodoPublic])
async def get_todos(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(Todo.user_id == current_user.id)
    result = await session.exec(statement)
    return result.all()

@app.post("/todos/", response_model=TodoPublic, status_code=201)
async def create_todo(
    todo: TodoCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_todo = Todo(**todo.dict(), user_id=current_user.id)
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo
```

## Testing

### TestClient
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

### Async Testing
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_todos():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/todos/")
    assert response.status_code == 200
```

### Override Dependencies
```python
def override_get_db():
    return test_db

app.dependency_overrides[get_db] = override_get_db
```

## Common Patterns

### Pagination
```python
@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 100):
    return items[skip : skip + limit]
```

### Filtering
```python
@app.get("/todos/")
async def get_todos(
    completed: bool | None = None,
    priority: int | None = None
):
    query = select(Todo)
    if completed is not None:
        query = query.where(Todo.completed == completed)
    if priority is not None:
        query = query.where(Todo.priority == priority)
    return await session.exec(query).all()
```

### Sorting
```python
@app.get("/todos/")
async def get_todos(sort_by: str = "created_at", order: str = "desc"):
    column = getattr(Todo, sort_by, Todo.created_at)
    query = select(Todo).order_by(
        column.desc() if order == "desc" else column
    )
    return await session.exec(query).all()
```

## Environment Variables

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    environment: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Usage
DATABASE_URL = settings.database_url
```

## Startup/Shutdown Events

```python
@app.on_event("startup")
async def startup_event():
    # Initialize database connection
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    # Close database connection
    await close_db()
```

## Quick Command Reference

| Task | Code |
|------|------|
| **Run app** | `uvicorn main:app --reload` |
| **Docs** | Visit `/docs` (Swagger UI) |
| **ReDoc** | Visit `/redoc` |
| **OpenAPI schema** | Visit `/openapi.json` |
| **Custom port** | `uvicorn main:app --port 8001` |
| **Custom host** | `uvicorn main:app --host 0.0.0.0` |

---

This reference covers 95% of FastAPI patterns you'll need for Phase 2. For advanced patterns, consult the SKILL.md or use the `using-context7` skill.