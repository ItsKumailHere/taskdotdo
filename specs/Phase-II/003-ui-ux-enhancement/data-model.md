# Data Model: Responsive UI/UX Enhancement & Task Management

**Feature**: Responsive UI/UX Enhancement & Task Management
**Date**: 2026-01-09
**Location**: /specs/Phase-II/003-ui-ux-enhancement/

## Database Schema Extensions

### User Preferences Table

```sql
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    theme VARCHAR(20) NOT NULL DEFAULT 'light' CHECK (theme IN ('light', 'dark', 'auto')),
    language VARCHAR(10) NOT NULL DEFAULT 'en',
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    notifications_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    dashboard_layout VARCHAR(20) NOT NULL DEFAULT 'default' CHECK (dashboard_layout IN ('default', 'compact', 'focus')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Relationships
- `user_preferences.user_id` references `users.id` (one-to-one relationship)
- When a user is deleted, their preferences are automatically deleted (CASCADE)

## SQLModel Definitions

### Theme Enum

```python
import enum

class ThemeOption(str, enum.Enum):
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"
```

### Dashboard Layout Enum

```python
class DashboardLayout(str, enum.Enum):
    DEFAULT = "default"
    COMPACT = "compact"
    FOCUS = "focus"
```

### UserPreferences Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

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

### Extended Todo Model (with search index)

```sql
-- Additional index for efficient searching
CREATE INDEX idx_todos_title_trgm ON todos USING gin(title gin_trgm_ops);
CREATE INDEX idx_todos_description_trgm ON todos USING gin(description gin_trgm_ops);
```

## Frontend Type Definitions

### User Preferences Interface

```typescript
interface UserPreferences {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  timezone: string;
  notificationsEnabled: boolean;
  dashboardLayout: 'default' | 'compact' | 'focus';
}

interface UpdateUserPreferencesRequest {
  theme?: 'light' | 'dark' | 'auto';
  language?: string;
  timezone?: string;
  notificationsEnabled?: boolean;
  dashboardLayout?: 'default' | 'compact' | 'focus';
}
```

### Task Query Parameters Interface

```typescript
interface TaskFilters {
  status?: 'all' | 'pending' | 'completed';
  sortBy?: 'created_at' | 'title' | 'due_date';
  order?: 'asc' | 'desc';
  search?: string;
  page?: number;
  limit?: number;
}
```