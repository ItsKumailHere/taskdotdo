# Quick Start Guide - Multi-User Todo Application

## Prerequisites

- Python 3.12+ with uv installed
- Node.js 18+ with npm
- Neon PostgreSQL database (see SETUP_GUIDE.md)

## 1. Environment Setup

### Backend Environment

Create `multi-user-todo/backend/.env`:

```bash
# Database (from Neon)
DATABASE_URL=postgresql+asyncpg://username:password@host.neon.tech/dbname

# Authentication (generate secure random string)
JWT_SECRET_KEY=your-super-secret-jwt-key-min-32-characters
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Application
ENVIRONMENT=development
```

**Generate JWT secret:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Frontend Environment

Create `multi-user-todo/frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 2. Start Backend

```bash
cd multi-user-todo/backend

# Install dependencies (if not already done)
uv sync

# Initialize database tables
uv run python -c "from app.database.database import init_db; import asyncio; asyncio.run(init_db())"

# Start server
uv run python main.py
```

Backend will run on **http://localhost:8000**

API documentation: **http://localhost:8000/docs**

## 3. Start Frontend

```bash
cd multi-user-todo/frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev
```

Frontend will run on **http://localhost:3000**

## 4. Test the Application

### Register a New User

1. Go to http://localhost:3000/register
2. Fill in:
   - **Email**: test@example.com
   - **Password**: testpass123 (minimum 8 characters)
   - **Username**: testuser
3. Click "Register"
4. You'll be redirected to the todos page

### Create Your First Todo

1. In the right sidebar, you'll see "Create New Todo"
2. Enter a description: "Buy groceries"
3. Optionally set a due date
4. Click "Add Todo"
5. Todo appears in the list!

### Manage Todos

- **Complete**: Click the checkbox to mark complete/incomplete
- **Edit**: Click "Edit" button, modify, click "Update Todo"
- **Delete**: Click "Delete" button, confirm in popup
- **Filter**: Use "All", "Active", "Completed" buttons

### Test Multi-User Isolation

1. Open an incognito window
2. Register a different user
3. Create todos for that user
4. Switch back to first user - you should only see your todos

## 5. Verify Everything Works

### Backend Health Check
```bash
curl http://localhost:8000/api/v1/health
# Should return: {"status":"healthy","version":"1.0.0"}
```

### Test Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test2@example.com",
    "password": "testpass123",
    "username": "test2"
  }'
```

### Test Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test2@example.com",
    "password": "testpass123"
  }'
```

Save the `access_token` from the response.

### Test Todo Creation
```bash
curl -X POST http://localhost:8000/api/v1/todos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "description": "Test todo from API"
  }'
```

### Test Todo Listing
```bash
curl http://localhost:8000/api/v1/todos/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 6. Common Issues

### Backend won't start - "DATABASE_URL not set"
- Make sure `.env` file exists in `backend/` directory
- Check that DATABASE_URL is set correctly

### Backend won't start - SSL error
- Verify DATABASE_URL doesn't have `?sslmode=require` at the end
- SSL is configured via `connect_args` in database.py

### Frontend can't connect to backend
- Make sure backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in `.env.local`
- Check CORS configuration in backend (should allow localhost:3000)

### "401 Unauthorized" errors
- Token may have expired (default: 7 days)
- Try logging in again
- Check that JWT_SECRET_KEY matches in backend

### Todos not appearing
- Check browser console for errors
- Verify you're logged in (check sessionStorage for auth_token)
- Try refreshing the page

## 7. Project Structure

```
multi-user-todo/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── auth/            # Auth utilities
│   │   ├── database/        # DB setup
│   │   ├── middleware/      # CORS, error handling
│   │   ├── models/          # SQLModel entities
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── utils/           # Errors, logger
│   ├── main.py              # FastAPI app entry
│   └── .env                 # Backend config
│
└── frontend/
    ├── app/                 # Next.js pages
    ├── components/          # React components
    ├── contexts/            # Auth context
    ├── lib/                 # API client, types, auth
    └── .env.local           # Frontend config
```

## 8. Available Features

✅ User registration and login
✅ JWT-based authentication
✅ Create, read, update, delete todos
✅ Mark todos as complete/incomplete
✅ Filter by status (all/active/completed)
✅ Set due dates on todos
✅ Real-time UI updates
✅ Multi-user isolation (users only see their own todos)
✅ Responsive design
✅ Error handling

## 9. Development Tips

### Backend Development
- API docs at http://localhost:8000/docs (interactive Swagger UI)
- Check logs for SQL queries (echo=True in database.py)
- Use `/health` endpoint to verify backend is running

### Frontend Development
- Hot reload enabled (changes reflect immediately)
- Check browser console for errors
- Use React DevTools to inspect component state

### Database Management
- View data directly in Neon console
- Use SQL console to run queries
- Check user_id on all records to verify isolation

## 10. Next Steps

Now that User Story 2 is complete, you can:
- Add categories and tags UI
- Implement todo-tag relationships
- Add search and advanced filtering
- Set up production deployment
- Add tests (pytest for backend, Jest for frontend)
- Implement notifications
- Add user preferences/settings

## Support

For issues:
1. Check SETUP_GUIDE.md for detailed setup instructions
2. Check USER_STORY_2_COMPLETE.md for implementation details
3. Check backend logs for errors
4. Check browser console for frontend errors

Happy coding! 🚀
