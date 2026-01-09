# TaskDo - Full Stack Todo Application

TaskDo is a modern full-stack todo application built with Next.js 16 (App Router) for the frontend and FastAPI with SQLModel for the backend. The application features JWT-based authentication and authorization, providing a secure and responsive user experience.

## 🚀 Features

- **User Authentication & Authorization**: Secure login, registration, and session management with JWT tokens
- **Todo Management**: Create, read, update, and delete todo items
- **Responsive UI**: Mobile-first design using Tailwind CSS
- **Real-time Updates**: Live synchronization of todo lists
- **Secure API**: Protected endpoints with JWT validation

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT

### Backend
- **Framework**: FastAPI
- **Database ORM**: SQLModel
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: Better Auth with JWT
- **Language**: Python 3.12

## 📁 Project Structure

```
Phase-II/
├── backend/              # FastAPI backend server
│   ├── app/              # Application code
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utility functions
│   ├── tests/            # Backend tests
│   └── main.py           # Application entry point
├── frontend/             # Next.js frontend application
│   ├── app/              # App Router pages
│   ├── components/       # Reusable UI components
│   ├── lib/              # Shared utilities
│   └── public/           # Static assets
└── specs/                # Feature specifications
    └── Phase-II/         # Phase II specifications
        └── [feature-name]/ # Individual feature specs
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.12+ (for backend)
- uv (Python package manager) or pip
- PostgreSQL database (Neon recommended)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd Phase-II/backend
   ```

2. Install dependencies:
   ```bash
   uv sync --all-extras  # If using uv
   # OR
   pip install -e '.[dev]'  # If using pip
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and JWT secrets
   ```

4. Run the development server:
   ```bash
   uv run dev  # If using uv with the script defined in pyproject.toml
   # OR
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd Phase-II/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your backend API URL
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## 🧪 Testing

### Backend Testing

Run backend tests with pytest:
```bash
# From the backend directory
uv run test  # If using uv with the script defined in pyproject.toml
# OR
pytest
```

### Frontend Testing

Run frontend tests:
```bash
# From the frontend directory
npm run test
```

## 🛠️ Linting and Formatting

### Backend
```bash
# Lint the codebase
uv run lint

# Format the codebase
uv run format

# Run type checking
uv run type-check
```

### Frontend
```bash
# Lint the codebase
npm run lint:check

# Automatically fix lint issues
npm run lint:fix

# Format the codebase
npm run format

# Check formatting without changing files
npm run format:check
```

## 📋 Feature Specifications

All feature specifications are located in the `specs/Phase-II/` directory, organized by feature:

- `001-user-auth/` - User authentication and authorization
- `002-todo-crud/` - Todo creation, reading, updating, and deletion
- `003-collaboration/` - Collaborative features (if applicable)

Each feature directory contains:
- `spec.md` - Detailed feature specification
- `plan.md` - Technical implementation plan
- `tasks.md` - Implementation tasks
- `contracts/` - API contracts
- `research.md` - Research and alternatives considered

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.