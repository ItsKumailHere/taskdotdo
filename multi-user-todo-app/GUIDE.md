# Multi-User Todo Application - Setup and Testing Guide

This guide will walk you through setting up, running, and manually testing the multi-user todo application.

## Prerequisites

Before starting, ensure you have the following installed on your system:

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn
- PostgreSQL (or access to a PostgreSQL database)
- Git

## Manual Setup Steps

### 1. Environment Configuration

You need to manually set up environment variables for both the backend and frontend:

#### Backend Environment Variables

Create a `.env` file in the `multi-user-todo-app/backend/` directory with the following content:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=129600  # 90 days in minutes
NEON_DATABASE_URL=your-neon-database-url
DEBUG=True
FRONTEND_URL=http://localhost:3000
```

**Important Notes:**
- Replace `username:password@localhost:5432/todo_app` with your actual PostgreSQL connection details
- Generate a secure `SECRET_KEY` for production use
- If using Neon Serverless Postgres, update the `NEON_DATABASE_URL`

#### Frontend Environment Variables

Create a `.env.local` file in the `multi-user-todo-app/frontend/` directory with the following content:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Database Setup

You need to manually set up your PostgreSQL database:

1. Install and start PostgreSQL on your system
2. Create a database for the application:
   ```sql
   CREATE DATABASE todo_app;
   ```
3. Create a database user with appropriate permissions:
   ```sql
   CREATE USER your_username WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE todo_app TO your_username;
   ```

## Running the Application

### 1. Backend Setup and Run

1. Navigate to the backend directory:
   ```bash
   cd multi-user-todo-app/backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -e .
   ```

   Or if you're using the system Python:
   ```bash
   python3 -m pip install --break-system-packages -e .
   ```

3. Start the backend server:
   ```bash
   python3 -m uvicorn main:app --reload --port 8000
   ```

The backend server will be available at `http://localhost:8000`.

**Note**: Better Auth is a frontend authentication library that runs on the client side. The backend simply verifies the JWT tokens that Better Auth generates using the shared secret.

### 2. Frontend Setup and Run

1. Navigate to the frontend directory:
   ```bash
   cd multi-user-todo-app/frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`.

## Manual Testing Guide

### 1. API Testing via Swagger UI

1. Once the backend is running, navigate to `http://localhost:8000/docs` in your browser
2. You can test all API endpoints directly from the Swagger UI interface
3. The API documentation includes all endpoints for:
   - Authentication (register, login, logout)
   - User management (get current user, update preferences)
   - Todo management (CRUD operations)
   - Category management
   - Tag management
   - Notification management

### 2. Frontend Testing

#### User Registration and Login
1. Open your browser and navigate to `http://localhost:3000`
2. Click on "Register" in the navigation bar
3. Fill in the registration form with:
   - Email: A valid email address
   - Username: A unique username (3-30 characters, alphanumeric and underscores only)
   - Password: At least 8 characters with uppercase, lowercase, number, and special character
   - Confirm Password: Same as the password
4. Submit the form and verify you're redirected to the dashboard
5. Test login by logging out and logging back in

#### Todo Management
1. After logging in, go to the dashboard or todos page
2. Create a new todo by filling in the form:
   - Description: Enter a task description (max 500 characters)
   - Due Date: Optionally set a due date
3. Test marking todos as complete/incomplete
4. Test editing existing todos
5. Test deleting todos

#### Category and Tag Management
1. Create categories and tags through the UI
2. Assign categories and tags to your todos
3. Test filtering and organizing your todos

#### Theme Customization
1. Use the theme toggle button to switch between light and dark modes
2. Verify that the preference is saved and persists across sessions

### 3. Multi-User Testing

1. Register multiple user accounts with different email addresses
2. Verify that each user can only see their own todos, categories, and tags
3. Confirm that user data is properly isolated between accounts

### 4. Session Management Testing

1. Log in from one browser/device
2. Try to access the app from another browser/device - you should be redirected to login
3. Verify that sessions persist for the configured duration (90 days in the example)

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: 
   - Verify your PostgreSQL server is running
   - Check that your DATABASE_URL in the backend `.env` file is correct
   - Ensure the database user has appropriate permissions

2. **Backend Server Won't Start**:
   - Check that all Python dependencies are installed
   - Verify your environment variables are set correctly
   - Make sure port 8000 is not already in use

3. **Frontend Can't Connect to Backend**:
   - Verify the backend server is running
   - Check that `NEXT_PUBLIC_API_URL` in the frontend `.env.local` matches your backend URL
   - Ensure both servers are running simultaneously

4. **CORS Errors**:
   - The backend is configured to allow requests from `http://localhost:3000`
   - If using a different frontend URL, update the `FRONTEND_URL` in the backend `.env` file

## API Endpoints Reference

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/logout` - Logout user

### User Management
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me/preferences` - Update user preferences

### Todo Management
- `GET /api/v1/todos` - Get all user's todos
- `POST /api/v1/todos` - Create new todo
- `GET /api/v1/todos/{id}` - Get specific todo
- `PUT /api/v1/todos/{id}` - Update specific todo
- `DELETE /api/v1/todos/{id}` - Delete specific todo

### Categories
- `GET /api/v1/categories` - Get all user's categories
- `POST /api/v1/categories` - Create new category

### Tags
- `GET /api/v1/tags` - Get all user's tags
- `POST /api/v1/tags` - Create new tag

## Production Considerations

When deploying to production, remember to:

1. Use strong, randomly generated secrets for `SECRET_KEY`
2. Configure proper SSL certificates
3. Set up a production-grade database with backups
4. Configure a reverse proxy (nginx, Apache)
5. Set `DEBUG=False` in production
6. Use environment variables for sensitive configuration
7. Implement proper logging and monitoring
8. Set up automated backups for your database