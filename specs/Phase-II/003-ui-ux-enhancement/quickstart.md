# Quickstart Guide: Responsive UI/UX Enhancement & Task Management

**Feature**: Responsive UI/UX Enhancement & Task Management
**Date**: 2026-01-09
**Location**: /specs/Phase-II/003-ui-ux-enhancement/

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or Neon Serverless Postgres)
- Next.js 16+
- Completed User Authentication & Authorization feature
- Completed Task CRUD Operations feature

## Setup Instructions

### Backend Setup (FastAPI)

1. Install additional dependencies (if not already installed):
```bash
pip install fastapi sqlmodel python-jose[cryptography] passlib[bcrypt] python-multipart
```

2. Create the UserPreferences model in `backend/app/models/user_preferences.py`:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
import enum

class ThemeOption(str, enum.Enum):
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"

class DashboardLayout(str, enum.Enum):
    DEFAULT = "default"
    COMPACT = "compact"
    FOCUS = "focus"

class UserPreferencesBase(SQLModel):
    theme: ThemeOption = Field(default=ThemeOption.LIGHT)
    language: str = Field(default="en", max_length=10)
    timezone: str = Field(default="UTC", max_length=50)
    notifications_enabled: bool = Field(default=True)
    dashboard_layout: DashboardLayout = Field(default=DashboardLayout.DEFAULT)

class UserPreferences(UserPreferencesBase, table=True):
    __tablename__ = "user_preferences"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationship to user
    user: "User" = Relationship(back_populates="preferences")
```

3. Create the API endpoints in `backend/app/api/v1/user_preferences.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from backend.app.models.user_preferences import UserPreferences, UserPreferencesBase
from backend.app.database import get_session
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.get("/", response_model=UserPreferences)
async def get_user_preferences(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    preferences = session.query(UserPreferences).filter(UserPreferences.user_id == current_user.id).first()
    if not preferences:
        # Create default preferences if they don't exist
        preferences = UserPreferences(user_id=current_user.id)
        session.add(preferences)
        session.commit()
        session.refresh(preferences)
    return preferences

@router.put("/", response_model=UserPreferences)
async def update_user_preferences(
    preferences_update: UserPreferencesBase,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    preferences = session.query(UserPreferences).filter(UserPreferences.user_id == current_user.id).first()
    if not preferences:
        preferences = UserPreferences(user_id=current_user.id, **preferences_update.dict())
        session.add(preferences)
    else:
        for key, value in preferences_update.dict(exclude_unset=True).items():
            setattr(preferences, key, value)
    
    session.commit()
    session.refresh(preferences)
    return preferences
```

4. Update the Todo API in `backend/app/api/v1/todos.py` to support filtering, sorting, and search:
```python
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from backend.app.models.todo import Todo, TaskStatus
from backend.app.database import get_session
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.get("/")
async def get_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    sort_by: str = Query("created_at", description="Sort by field"),
    order: str = Query("desc", description="Sort order"),
    search: Optional[str] = Query(None, description="Search term for title/description"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
):
    # Build the query
    query = select(Todo).where(Todo.user_id == current_user.id)
    
    # Apply status filter
    if status:
        query = query.where(Todo.status == status)
    
    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (Todo.title.ilike(search_pattern)) | 
            (Todo.description.ilike(search_pattern))
        )
    
    # Apply sorting
    if sort_by == "title":
        sort_field = Todo.title
    elif sort_by == "due_date":
        sort_field = Todo.due_date
    else:  # default to created_at
        sort_field = Todo.created_at
    
    if order == "asc":
        query = query.order_by(sort_field)
    else:
        query = query.order_by(sort_field.desc())
    
    # Apply pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    
    todos = session.exec(query).all()
    
    # Get total count for pagination info
    count_query = select(func.count(Todo.id)).where(Todo.user_id == current_user.id)
    if status:
        count_query = count_query.where(Todo.status == status)
    if search:
        search_pattern = f"%{search}%"
        count_query = count_query.where(
            (Todo.title.ilike(search_pattern)) | 
            (Todo.description.ilike(search_pattern))
        )
    total = session.exec(count_query).one()
    
    return {
        "data": todos,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }
```

### Frontend Setup (Next.js)

1. Install additional dependencies:
```bash
npm install clsx tailwind-merge lucide-react
# For theme management
npm install next-themes
```

2. Configure Tailwind CSS in `tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
  darkMode: 'class', // Enable dark mode with class strategy
}
```

3. Create theme provider component in `frontend/components/theme-provider.tsx`:
```tsx
"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { type ThemeProviderProps } from "next-themes/dist/types";

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}
```

4. Create a theme toggle component in `frontend/components/theme-toggle.tsx`:
```tsx
"use client";

import * as React from "react";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

import { Button } from "@/components/ui/button";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
```

5. Create task filter component in `frontend/components/task-filter.tsx`:
```tsx
"use client";

import { TaskStatus } from "@/lib/types/todo";

interface TaskFilterProps {
  currentFilter: TaskStatus | "all";
  onFilterChange: (filter: TaskStatus | "all") => void;
}

export function TaskFilter({ currentFilter, onFilterChange }: TaskFilterProps) {
  return (
    <div className="flex space-x-2 mb-4">
      {(["all", "pending", "completed"] as const).map((filter) => (
        <button
          key={filter}
          className={`px-4 py-2 rounded-md ${
            currentFilter === filter
              ? "bg-blue-500 text-white"
              : "bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200"
          }`}
          onClick={() => onFilterChange(filter)}
        >
          {filter.charAt(0).toUpperCase() + filter.slice(1)}
        </button>
      ))}
    </div>
  );
}
```

6. Create task sort component in `frontend/components/task-sort.tsx`:
```tsx
"use client";

interface TaskSortProps {
  currentSort: string;
  currentOrder: string;
  onSortChange: (sort: string, order: string) => void;
}

export function TaskSort({ currentSort, currentOrder, onSortChange }: TaskSortProps) {
  return (
    <div className="flex space-x-2 mb-4">
      <select
        value={currentSort}
        onChange={(e) => onSortChange(e.target.value, currentOrder)}
        className="border rounded-md p-2 dark:bg-gray-700 dark:text-white"
      >
        <option value="created_at">Sort by Date</option>
        <option value="title">Sort by Title</option>
        <option value="due_date">Sort by Due Date</option>
      </select>
      
      <select
        value={currentOrder}
        onChange={(e) => onSortChange(currentSort, e.target.value)}
        className="border rounded-md p-2 dark:bg-gray-700 dark:text-white"
      >
        <option value="asc">Ascending</option>
        <option value="desc">Descending</option>
      </select>
    </div>
  );
}
```

7. Create search component in `frontend/components/search-bar.tsx`:
```tsx
"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";

interface SearchBarProps {
  onSearch: (query: string) => void;
}

export function SearchBar({ onSearch }: SearchBarProps) {
  const [query, setQuery] = useState("");

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      onSearch(query);
    }, 300); // Debounce search by 300ms

    return () => clearTimeout(timeoutId);
  }, [query, onSearch]);

  return (
    <div className="mb-4">
      <Input
        type="text"
        placeholder="Search tasks..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full"
      />
    </div>
  );
}
```

8. Update your main layout in `frontend/app/layout.tsx` to include the theme provider:
```tsx
import { ThemeProvider } from "@/components/theme-provider";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "TaskDo - Task Management App",
  description: "A sleek todoist-style task management application",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

9. Create a responsive navigation component in `frontend/components/responsive-nav.tsx`:
```tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Menu, X } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export function ResponsiveNav() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const pathname = usePathname();

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  return (
    <nav className="bg-white dark:bg-gray-800 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/dashboard" className="text-xl font-bold text-blue-500">
              TaskDo
            </Link>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            <Link href="/dashboard">
              <Button variant={pathname === '/dashboard' ? 'default' : 'ghost'}>
                Dashboard
              </Button>
            </Link>
            <Link href="/tasks">
              <Button variant={pathname === '/tasks' ? 'default' : 'ghost'}>
                Tasks
              </Button>
            </Link>
          </div>
          
          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <Button variant="ghost" onClick={toggleMenu}>
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>
        
        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              <Link href="/dashboard">
                <Button 
                  variant={pathname === '/dashboard' ? 'default' : 'ghost'} 
                  className="w-full justify-start"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Dashboard
                </Button>
              </Link>
              <Link href="/tasks">
                <Button 
                  variant={pathname === '/tasks' ? 'default' : 'ghost'} 
                  className="w-full justify-start"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Tasks
                </Button>
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
```

These implementations will provide the responsive UI/UX enhancements and task management features as specified in the feature requirements.