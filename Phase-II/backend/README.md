# TaskDo Backend

The backend for the TaskDo application is built with FastAPI and SQLModel, providing a robust and efficient API for the todo application.

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database ORM**: SQLModel
- **Database**: PostgreSQL (Neon Serverless compatible)
- **Authentication**: Better Auth with JWT
- **Language**: Python 3.12
- **Testing**: pytest

## 📁 Directory Structure

```
backend/
├── app/                  # Application code
│   ├── api/              # API routes and endpoints
│   │   └── v1/           # API version 1
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas for request/response validation
│   ├── services/         # Business logic and service layer
│   ├── utils/            # Utility functions
│   ├── middleware/       # Request/response middleware
│   └── config/           # Configuration management
├── tests/                # Test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── contract/         # Contract tests
├── main.py               # Application entry point
├── pyproject.toml        # Project dependencies and configuration
└── README.md             # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- uv (recommended) or pip
- PostgreSQL database (Neon Serverless recommended)

### Installation

1. Install dependencies:
   ```bash
   uv sync --all-extras  # If using uv
   # OR
   pip install -e '.[dev]'  # If using pip
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and JWT secrets
   ```

3. Run the development server:
   ```bash
   uv run dev  # If using uv with the script defined in pyproject.toml
   # OR
   uvicorn main:app --reload
   ```

### Environment Variables

The application requires the following environment variables:

- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql+asyncpg://user:password@localhost:5432/dbname`)
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing (minimum 32 characters)
- `FRONTEND_URL`: URL of the frontend application for CORS configuration
- `ENVIRONMENT`: Environment type (development, staging, production)

Copy `.env.example` to `.env` and update the values accordingly.

### Database Setup

For development, you can use Docker to run a PostgreSQL instance:

```bash
docker run --name taskdo-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=taskdo_dev -p 5432:5432 -d postgres:15
```

For production, it's recommended to use a managed PostgreSQL service like Neon, AWS RDS, or Google Cloud SQL.

## 🧪 Testing

Run the full test suite:
```bash
uv run test  # If using uv with the script defined in pyproject.toml
# OR
pytest
```

Run specific test types:
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Contract tests
pytest tests/contract/
```

## 🔧 Linting and Formatting

The backend uses several tools for code quality:

- **Ruff**: Fast Python linter and formatter
- **Black**: Code formatter
- **mypy**: Static type checker
- **pytest**: Testing framework

```bash
# Lint the codebase
uv run lint

# Format the codebase
uv run format

# Run type checking
uv run type-check
```

## 📡 API Documentation

Once the server is running, you can access:

- **Interactive API docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative API docs**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **API spec (JSON)**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## 🔐 Authentication

The backend implements JWT-based authentication:

1. Users register/login via the auth endpoints
2. Successful authentication returns a JWT token
3. Subsequent requests to protected endpoints must include the token in the `Authorization` header as `Bearer {token}`
4. The middleware validates the token and extracts user information

## 🗄️ Database

The application uses SQLModel (SQLAlchemy + Pydantic) for database operations:

- Models are defined in `app/models/`
- Migrations are handled through Alembic (to be set up)
- Connection pooling and async operations are supported

## 🚨 Error Handling

The backend follows consistent error response patterns:

- Standard HTTP status codes
- JSON error responses with `detail` field
- Custom exception handlers for different error types

## 📈 Environment Configuration

The application uses environment variables for configuration:

- `DATABASE_URL`: Database connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `JWT_ALGORITHM`: Algorithm for JWT encoding (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `ENVIRONMENT`: Environment (development, staging, production)

## 🤝 Contributing

1. Follow the linting and formatting standards
2. Write tests for new functionality
3. Update documentation as needed
4. Follow the existing code style and patterns