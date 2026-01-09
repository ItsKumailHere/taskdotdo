# Task.do - Frontend

A modern, multi-user todo application frontend built with Next.js 16 App Router, TypeScript, and a refined design system.

## Tech Stack

- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4 + Custom CSS Variables
- **Fonts**: DM Sans (primary), Space Mono (monospace)
- **Authentication**: Better Auth (JWT) - Phase 2
- **API Communication**: Native Fetch API with custom client

## Project Structure

```
frontend/
├── app/                      # Next.js App Router pages
│   ├── layout.tsx           # Root layout with global providers
│   ├── page.tsx             # Home/landing page
│   ├── globals.css          # Global styles & design system
│   ├── login/               # Authentication pages
│   ├── register/
│   ├── dashboard/           # Main dashboard
│   └── todos/               # Todo management pages
├── components/              # React components
│   ├── TodoItem.tsx
│   ├── TodoList.tsx
│   ├── TodoForm.tsx
│   ├── AuthForm.tsx
│   ├── Navbar.tsx
│   └── ThemeToggle.tsx
├── lib/                     # Utilities and helpers
│   ├── types.ts            # TypeScript type definitions
│   ├── api.ts              # API client for backend communication
│   └── auth.ts             # Authentication utilities
├── styles/                  # Additional style modules (if needed)
├── public/                  # Static assets
└── tests/                   # Test files
    ├── unit/
    └── integration/
```

## Design System

### Philosophy

Task.do uses a refined, productivity-focused aesthetic with:

- **Clean, editorial layouts** with generous whitespace
- **Monochrome base** (black & white) with strategic color accents
- **Sharp typography hierarchy** using DM Sans and Space Mono
- **Subtle animations** that enhance without distraction

### Color Palette

**Light Theme:**
- Background: `#fafafa`
- Foreground: `#0a0a0a`
- Accent colors for priority and status

**Dark Theme:**
- Background: `#0a0a0a`
- Foreground: `#fafafa`
- Enhanced contrast with adjusted shadows

### CSS Variables

All design tokens are available as CSS custom properties:

```css
/* Colors */
--background, --foreground
--primary, --secondary
--destructive, --success, --warning

/* Priority & Status */
--priority-low, --priority-medium, --priority-high, --priority-urgent
--status-pending, --status-progress, --status-completed

/* Spacing */
--space-xs through --space-3xl

/* Border Radius */
--radius-sm through --radius-xl

/* Shadows */
--shadow-sm through --shadow-xl

/* Transitions */
--transition-fast, --transition-base, --transition-slow
```

### Typography Scale

- H1: 48px (3rem) - Page titles
- H2: 36px (2.25rem) - Section headers
- H3: 30px (1.875rem) - Subsection headers
- H4: 24px (1.5rem) - Component headers
- H5: 20px (1.25rem) - Small headers
- H6: 16px (1rem) - Labels (uppercase)
- Body: 16px (1rem) - Default text

## Getting Started

### Prerequisites

- Node.js 20+ (LTS recommended)
- npm, yarn, pnpm, or bun

### Installation

1. **Install dependencies:**

```bash
npm install
# or
pnpm install
# or
yarn install
```

2. **Set up environment variables:**

```bash
cp .env.example .env.local
```

Edit `.env.local` and configure:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

3. **Run the development server:**

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

### Development Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Run ESLint
npm run lint

# Run tests (when configured)
npm run test
```

## API Client

The frontend communicates with the FastAPI backend using a custom API client located in `lib/api.ts`.

### Usage Example

```typescript
import { apiClient } from "@/lib/api"

// Get all todos
const response = await apiClient.todos.getAll()
if (response.data) {
  console.log(response.data.todos)
}

// Create a new todo
const newTodo = await apiClient.todos.create({
  title: "Complete project",
  priority: "high",
  due_date: "2024-12-31"
})

// Authentication
const loginResult = await apiClient.auth.login({
  email: "user@example.com",
  password: "password123"
})
```

### API Client Structure

- `authApi` - Authentication endpoints (login, register, logout)
- `todoApi` - Todo CRUD operations
- `categoryApi` - Category management
- `tagApi` - Tag management

All methods return `ApiResponse<T>` with consistent error handling.

## Type Safety

The application uses comprehensive TypeScript types defined in `lib/types.ts`:

- `User`, `Todo`, `Category`, `Tag`, `Notification`
- Input/output types for API operations
- Enum types for status and priority
- Component prop types

## Authentication (Phase 2)

Authentication will be implemented using Better Auth with JWT tokens:

1. User logs in via Better Auth
2. JWT token is generated and stored
3. Token is included in all API requests
4. Backend verifies token and returns user-specific data

See `lib/auth.ts` for authentication utilities (placeholder for now).

## Styling Guidelines

### Using CSS Variables

```tsx
// In your components
<div style={{
  background: "var(--background)",
  color: "var(--foreground)",
  padding: "var(--space-lg)"
}}>
  Content
</div>
```

### Using Utility Classes

```tsx
// Predefined utility classes from globals.css
<div className="card animate-fade-in">
  <span className="badge badge-success">Completed</span>
</div>
```

### Custom Animations

Available animation classes:
- `.animate-fade-in`
- `.animate-slide-up`
- `.animate-slide-down`
- `.animate-scale-in`
- `.animate-spin`
- `.animate-stagger` (for list items)

## Component Guidelines

### Server Components (Default)

Most components should be Server Components for optimal performance:

```tsx
// app/dashboard/page.tsx
export default async function DashboardPage() {
  // Can directly fetch data here
  const todos = await fetchTodos()

  return <div>{/* ... */}</div>
}
```

### Client Components

Use `"use client"` only when needed for:
- Browser APIs (localStorage, window)
- React hooks (useState, useEffect)
- Event handlers
- Interactive UI

```tsx
"use client"

import { useState } from "react"

export function TodoForm() {
  const [title, setTitle] = useState("")
  // Component logic...
}
```

## Performance Optimization

- Server Components by default for faster initial load
- Strategic use of Client Components
- CSS-only animations where possible
- Image optimization with next/image
- Font optimization with next/font

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Accessibility

- Semantic HTML structure
- ARIA labels where needed
- Keyboard navigation support
- Focus management
- Screen reader compatibility

## Future Enhancements

- [ ] Dark/light theme toggle component
- [ ] Better Auth integration
- [ ] Real-time updates (WebSocket/SSE)
- [ ] Offline support (PWA)
- [ ] Keyboard shortcuts
- [ ] Drag-and-drop todo reordering
- [ ] Bulk operations
- [ ] Advanced filtering and search

## Related Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Better Auth Documentation](https://better-auth.com) (Phase 2)

## Contributing

When contributing to the frontend:

1. Follow the established design system
2. Use TypeScript strictly (no `any` types)
3. Prefer Server Components unless client interaction is required
4. Write semantic, accessible HTML
5. Test across supported browsers
6. Document complex logic with comments

## License

Part of the Task.do multi-user todo application.
