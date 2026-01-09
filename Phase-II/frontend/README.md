# TaskDo Frontend

The frontend for the TaskDo application is built with Next.js 16 using the App Router, providing a modern and responsive user interface.

## 🛠️ Tech Stack

- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT
- **Testing**: Jest, React Testing Library

## 📁 Directory Structure

```
frontend/
├── app/                    # App Router pages and layouts
│   ├── api/                # API routes (if any server-side logic)
│   ├── auth/               # Authentication-related pages
│   ├── dashboard/          # Main dashboard page
│   ├── login/              # Login page
│   ├── register/           # Registration page
│   └── globals.css         # Global styles
├── components/             # Reusable UI components
│   ├── auth/               # Authentication components
│   ├── todo/               # Todo-specific components
│   └── ui/                 # Generic UI components
├── lib/                    # Shared utilities and constants
│   ├── api.ts              # API client utilities
│   ├── auth.ts             # Authentication utilities
│   └── types.ts            # TypeScript type definitions
├── public/                 # Static assets
├── hooks/                  # Custom React hooks (if any)
├── .env.local              # Local environment variables
├── next.config.ts          # Next.js configuration
├── tailwind.config.ts      # Tailwind CSS configuration
├── tsconfig.json           # TypeScript configuration
├── package.json            # Dependencies and scripts
├── eslint.config.mjs       # ESLint configuration
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- npm, yarn, or bun

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your backend API URL
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## 🧪 Testing

Run the test suite:
```bash
npm run test
```

Run tests in watch mode:
```bash
npm run test -- --watch
```

## 🔧 Linting and Formatting

The frontend uses several tools for code quality:

- **ESLint**: JavaScript/TypeScript linter
- **Prettier**: Code formatter
- **TypeScript**: Type checking

```bash
# Check for linting errors
npm run lint:check

# Automatically fix linting issues
npm run lint:fix

# Format all files
npm run format

# Check formatting without changing files
npm run format:check
```

## 🏗️ Architecture

### Pages (App Router)

The application uses Next.js App Router for routing:

- `app/page.tsx` - Landing page
- `app/login/page.tsx` - Login page
- `app/register/page.tsx` - Registration page
- `app/dashboard/page.tsx` - Main dashboard with todos
- `app/layout.tsx` - Root layout component

### Components

Reusable components are organized by functionality:

- `components/auth/` - Login, registration forms, and auth providers
- `components/todo/` - Todo list, todo item, and todo form components
- `components/ui/` - Generic UI elements like buttons, modals, etc.

### Utilities

Shared utilities in the `lib/` directory:

- `lib/api.ts` - API client and request utilities
- `lib/auth.ts` - Authentication helpers and token management
- `lib/types.ts` - Shared TypeScript type definitions

#### Authentication Utilities

The `lib/auth.ts` file provides utilities for managing authentication state:

- `isAuthenticated()` - Check if user is currently authenticated
- `getToken()` / `storeToken()` / `removeToken()` - Manage JWT tokens in storage
- `getAuthHeader()` - Get authorization header with current token
- `login()` / `logout()` / `register()` - Authentication flow functions
- `getUserFromToken()` - Extract user information from JWT token
- `isTokenExpired()` - Check if JWT token is expired

#### API Client

The `lib/api.ts` file provides a wrapper around the fetch API for making requests to the backend:

- `ApiClient` class for making HTTP requests
- Automatic inclusion of authentication headers
- Error handling and response parsing

## 🎨 Styling

The application uses Tailwind CSS for styling with the following principles:

- Mobile-first responsive design
- Consistent color palette defined in `tailwind.config.ts`
- Component-specific styling using utility classes
- Dark mode support (if implemented)

## 🔐 Authentication

The frontend handles authentication using Better Auth:

1. Users authenticate via login/register pages
2. JWT tokens are stored securely (preferably in httpOnly cookies)
3. Protected routes use authentication guards
4. API requests include authentication headers automatically

## 📱 Responsive Design

The application is designed to be responsive across all device sizes:

- Mobile-first approach using Tailwind's responsive prefixes
- Touch-friendly interface elements
- Optimized for various screen sizes

## 🌐 Environment Variables

The application uses environment variables for configuration:

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
- `NEXT_PUBLIC_APP_NAME`: Name of the application
- Other environment-specific variables

## 🚨 Error Handling

The frontend implements consistent error handling:

- Global error boundaries for unexpected errors
- Form validation with user-friendly messages
- API error responses with appropriate feedback
- Loading states for async operations

## 🤝 Contributing

1. Follow the linting and formatting standards
2. Write tests for new components and functionality
3. Update documentation as needed
4. Follow the existing code style and patterns
5. Use TypeScript for type safety
6. Leverage Tailwind CSS utility classes for styling