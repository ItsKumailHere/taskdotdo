# Multi-User Todo Application

A full-stack web application for managing personal tasks with authentication, categorization, and customization features.

## Features

- **User Authentication**: Secure registration and login with JWT-based authentication
- **Todo Management**: Create, read, update, and delete todos with descriptions, due dates, tags, and categories
- **Organization**: Filter and sort todos by tags, categories, and due dates
- **Customization**: Dark mode and theme preferences
- **Notifications**: Browser-based notifications for upcoming due dates
- **Session Management**: Persistent sessions for up to 90 days with single-device login restriction

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLModel**: ORM for database interactions
- **Neon Serverless Postgres**: Scalable database solution
- **Better Auth**: JWT-based authentication
- **Pydantic**: Data validation and settings management

### Frontend
- **Next.js 16**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Better Auth**: Authentication integration

## Project Structure

```
multi-user-todo/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── models/   # Database models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   ├── database/ # Database configuration
│   │   └── config/   # Application settings
│   └── tests/        # Backend tests
└── frontend/         # Next.js frontend
    ├── app/          # Pages and layouts
    ├── components/   # React components
    ├── lib/          # Utilities
    └── styles/       # Global styles
```

## Setup Instructions

### Prerequisites

- Python 3.12+
- Node.js 18+
- Neon Postgres database account
- UV package manager for Python

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Copy the environment file and configure:
   ```bash
   cp .env.example .env
   ```

3. Set up your environment variables in `.env`:
   - `DATABASE_URL`: Your Neon Postgres connection string
   - `JWT_SECRET_KEY`: A secure random string (minimum 32 characters)
   - `SECRET_KEY`: Another secure random string for app security

4. Install dependencies:
   ```bash
   uv sync
   ```

5. Run database migrations (coming in Phase 2)

6. Start the backend server:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Copy the environment file and configure:
   ```bash
   cp .env.example .env.local
   ```

3. Set up your environment variables in `.env.local`:
   - `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000/api)

4. Install dependencies:
   ```bash
   npm install
   ```

5. Start the development server:
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:3000`

## Environment Configuration

### Required Environment Variables

#### Backend (.env)

- **DATABASE_URL**: PostgreSQL connection string from Neon
  - Format: `postgresql://user:password@host:5432/database`
  - Get this from your Neon dashboard

- **JWT_SECRET_KEY**: Secret key for JWT token signing
  - Must be at least 32 characters
  - Generate with: `openssl rand -hex 32`

- **SECRET_KEY**: Application secret key
  - Must be at least 32 characters
  - Generate with: `openssl rand -hex 32`

#### Frontend (.env.local)

- **NEXT_PUBLIC_API_URL**: Backend API URL
  - Development: `http://localhost:8000/api`
  - Production: Your deployed backend URL

## Development

### Code Quality

- **Backend**:
  - Linting: `uv run ruff check .`
  - Formatting: `uv run ruff format .`

- **Frontend**:
  - Linting: `npm run lint`
  - Formatting: `npm run format`

### Testing

- **Backend**: `uv run pytest`
- **Frontend**: `npm test`

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Implementation Phases

- **Phase 1**: Setup ✅
- **Phase 2**: Foundational infrastructure (In Progress)
- **Phase 3**: User registration and authentication
- **Phase 4**: Todo management
- **Phase 5**: Organization and filtering
- **Phase 6**: UX customization
- **Phase 7**: Session management
- **Phase 8**: Polish and optimization

## License

MIT

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.
