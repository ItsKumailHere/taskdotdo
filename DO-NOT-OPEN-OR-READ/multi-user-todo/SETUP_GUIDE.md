# Multi-User Todo Application - Setup Guide

This guide provides step-by-step instructions for setting up the required API keys, database, and environment variables for the Multi-User Todo Application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Database Setup (Neon PostgreSQL)](#database-setup-neon-postgresql)
- [Environment Variables](#environment-variables)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.12+** (for backend)
- **uv** (Python package manager) - Install via: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Node.js 18+** (for frontend)
- **npm** or **pnpm** or **yarn** (package manager for frontend)
- **Git** (version control)

---

## Database Setup (Neon PostgreSQL)

### Step 1: Create a Neon Account

1. Visit [https://neon.tech](https://neon.tech)
2. Sign up for a free account
3. Verify your email address

### Step 2: Create a New Project

1. Click "New Project" in your Neon dashboard
2. **Project Name**: `multi-user-todo` (or your preferred name)
3. **Region**: Select the region closest to you
4. **Postgres Version**: Use the default (latest version)
5. Click "Create Project"

### Step 3: Get Your Connection String

1. In your project dashboard, click on "Connection Details"
2. Copy the **Connection String** (it should look like this):
   ```
   postgresql://username:password@host.neon.tech/database?sslmode=require
   ```
3. **IMPORTANT**: Save this connection string securely - you'll need it for the backend `.env` file

### Step 4: Modify Connection String for asyncpg

The connection string from Neon uses `postgresql://`, but our backend uses the `asyncpg` driver.
You need to make TWO changes:

1. Replace `postgresql://` with `postgresql+asyncpg://`
2. **Remove** `?sslmode=require` from the end (SSL is configured in the engine)

**Original from Neon:**
```
postgresql://username:password@ep-xxx-123.us-east-2.aws.neon.tech/database?sslmode=require
```

**Modified for Backend:**
```
postgresql+asyncpg://username:password@ep-xxx-123.us-east-2.aws.neon.tech/database
```

**Important**: Do NOT include `?sslmode=require` - asyncpg doesn't accept this parameter in the URL. SSL is automatically configured to "require" mode in the engine settings.

---

## Environment Variables

### Backend Environment Variables

1. Navigate to the backend directory:
   ```bash
   cd multi-user-todo/backend
   ```

2. Create a `.env` file by copying the example:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and fill in the following values:

```bash
# Database Configuration
# Use the MODIFIED connection string from Neon (with postgresql+asyncpg://)
# IMPORTANT: Remove ?sslmode=require from the URL
DATABASE_URL=postgresql+asyncpg://username:password@host.neon.tech/database

# JWT Configuration
# Generate a strong secret key (minimum 32 characters)
# You can use: python -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_SECRET_KEY=your-super-secret-jwt-key-min-32-characters-change-this
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=43200  # 30 days
JWT_REFRESH_TOKEN_EXPIRE_DAYS=90

# CORS Configuration
# Add your frontend URL(s) here (comma-separated for multiple)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Application Configuration
APP_NAME="Multi-User Todo Application"
APP_VERSION="1.0.0"
DEBUG=True  # Set to False in production
ENVIRONMENT=development  # Change to 'production' when deploying

# Security
# Generate another strong secret key for general app security
# You can use: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-app-secret-key-min-32-characters-change-this

# Session Configuration
SESSION_EXPIRE_DAYS=90
SINGLE_DEVICE_LOGIN=True
```

#### How to Generate Secure Keys:

**Using Python:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Using OpenSSL:**
```bash
openssl rand -base64 32
```

**Using Online Generator:**
- Visit [https://randomkeygen.com/](https://randomkeygen.com/)
- Use the "CodeIgniter Encryption Keys" section

### Frontend Environment Variables

1. Navigate to the frontend directory:
   ```bash
   cd multi-user-todo/frontend
   ```

2. Create a `.env.local` file by copying the example:
   ```bash
   cp .env.example .env.local
   ```

3. Edit `.env.local` and fill in the following values:

```bash
# API Configuration
# This should point to your backend API
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Better Auth Configuration (for Phase 2+)
# MUST match the backend JWT_SECRET_KEY exactly
BETTER_AUTH_SECRET=your-super-secret-jwt-key-min-32-characters-change-this
BETTER_AUTH_URL=http://localhost:3000

# Environment
NODE_ENV=development  # Change to 'production' when deploying
```

**CRITICAL**: The `BETTER_AUTH_SECRET` in frontend MUST match `JWT_SECRET_KEY` in backend!

---

## Backend Setup

### Step 1: Install Dependencies

```bash
cd multi-user-todo/backend
uv sync
```

This will:
- Create a virtual environment
- Install all required Python packages
- Lock dependencies in `uv.lock`

### Step 2: Initialize Database

The database tables will be created automatically when you start the backend server for the first time. The `init_db()` function in `app/database/database.py` handles this.

### Step 3: Verify Installation

Test that everything is configured correctly:

```bash
uv run python -c "from app.config.settings import settings; print('✓ Settings loaded successfully')"
```

If you see "✓ Settings loaded successfully", you're good to go!

---

## Frontend Setup

### Step 1: Install Dependencies

```bash
cd multi-user-todo/frontend
npm install
# or
pnpm install
# or
yarn install
```

### Step 2: Verify Installation

```bash
npm run build
# or
pnpm build
# or
yarn build
```

If the build succeeds, your frontend is configured correctly!

---

## Running the Application

### Start Backend Server

```bash
cd multi-user-todo/backend
uv run python main.py
```

The backend API will start on `http://localhost:8000`

**Verify backend is running:**
- Visit: `http://localhost:8000` - Should show API info
- Visit: `http://localhost:8000/health` - Should return `{"status":"healthy"}`
- Visit: `http://localhost:8000/docs` - Should show interactive API documentation (Swagger UI)

### Start Frontend Development Server

In a new terminal:

```bash
cd multi-user-todo/frontend
npm run dev
# or
pnpm dev
# or
yarn dev
```

The frontend will start on `http://localhost:3000`

**Verify frontend is running:**
- Visit: `http://localhost:3000` - Should load the home page

---

## Troubleshooting

### Database Connection Issues

**Error: "Could not connect to database"** or **"TypeError: connect() got an unexpected keyword argument 'sslmode'"**

1. Verify your `DATABASE_URL` is correct
2. Ensure you're using `postgresql+asyncpg://` (not just `postgresql://`)
3. **IMPORTANT**: Remove `?sslmode=require` from the connection string - asyncpg doesn't accept this parameter
4. Verify your Neon project is active (not suspended)
5. Check your internet connection
6. Make sure your connection string format is exactly:
   ```
   postgresql+asyncpg://user:password@host.neon.tech/database
   ```
   (No `?sslmode=require` at the end!)

**Solution:**
```bash
# Test connection manually
   uv run python -c "from app.database.database import engine; import asyncio; asyncio.run(engine.connect())"
```

### JWT Secret Key Mismatch

**Error: "Could not validate credentials" or "Invalid token"**

This happens when frontend and backend have different secret keys.

**Solution:**
1. Make sure `BETTER_AUTH_SECRET` (frontend) matches `JWT_SECRET_KEY` (backend)
2. Both values must be EXACTLY the same
3. Restart both servers after making changes

### CORS Errors

**Error: "Access to fetch at ... has been blocked by CORS policy"**

**Solution:**
1. Verify `CORS_ORIGINS` in backend `.env` includes your frontend URL
2. Make sure there are no trailing slashes in URLs
3. Restart the backend server after changes

### Port Already in Use

**Error: "Address already in use"**

**Backend (port 8000):**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Frontend (port 3000):**
```bash
# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Environment Variables Not Loading

**Solution:**
1. Ensure `.env` file is in the correct directory:
   - Backend: `multi-user-todo/backend/.env`
   - Frontend: `multi-user-todo/frontend/.env.local`
2. Check file permissions (should be readable)
3. Restart servers after creating/modifying `.env` files
4. Verify no syntax errors in `.env` files (no spaces around `=`)

---

## Security Checklist

Before deploying to production:

- [ ] Change all secret keys from default values
- [ ] Use strong, randomly generated secrets (minimum 32 characters)
- [ ] Set `DEBUG=False` in backend `.env`
- [ ] Set `NODE_ENV=production` in frontend `.env`
- [ ] Update `CORS_ORIGINS` to include only your production frontend URL
- [ ] Never commit `.env` or `.env.local` files to Git
- [ ] Use environment variables in production (not `.env` files)
- [ ] Enable HTTPS for both frontend and backend
- [ ] Regularly rotate secret keys

---

## Production Deployment

### Backend Deployment (Example: Render/Railway/Fly.io)

1. Set environment variables in your hosting platform dashboard
2. Ensure `DATABASE_URL` points to your production Neon database
3. Set `ENVIRONMENT=production`
4. Set `DEBUG=False`
5. Update `CORS_ORIGINS` to include production frontend URL

### Frontend Deployment (Example: Vercel/Netlify)

1. Set environment variables in deployment platform
2. Update `NEXT_PUBLIC_API_URL` to your production backend URL
3. Ensure `BETTER_AUTH_SECRET` matches backend
4. Set `NODE_ENV=production`

---

## Quick Reference

### Backend URLs (Development)
- API Root: `http://localhost:8000`
- Health Check: `http://localhost:8000/health`
- API v1: `http://localhost:8000/api/v1`
- API Docs: `http://localhost:8000/docs`

### Frontend URLs (Development)
- Home: `http://localhost:3000`
- Login: `http://localhost:3000/login`
- Register: `http://localhost:3000/register`
- Dashboard: `http://localhost:3000/dashboard`

### Important Commands

**Backend:**
```bash
# Start server
uv run python main.py

# Run with auto-reload
uv run uvicorn main:app --reload

# Create new migration (if using Alembic)
uv run alembic revision --autogenerate -m "description"
```

**Frontend:**
```bash
# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start
```

---

## Next Steps

After completing this setup:

1. ✅ Test backend health endpoint: `http://localhost:8000/health`
2. ✅ Check API documentation: `http://localhost:8000/docs`
3. ✅ Verify frontend loads: `http://localhost:3000`
4. ✅ Proceed with Phase 3 implementation (User Stories)

---

## Support

If you encounter issues not covered in this guide:

1. Check the application logs (backend terminal output)
2. Check browser console for frontend errors
3. Verify all environment variables are set correctly
4. Ensure both backend and frontend servers are running

**Phase 2 Foundation Complete!** 🎉

The core infrastructure is now ready for Phase 3 user story implementation.
