# Tasks: User Authentication & Authorization

**Input**: Design documents from `/specs/Phase-II/001-user-auth/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/` at repository root
- **Backend**: `backend/app/`, `backend/tests/`
- **Frontend**: `frontend/app/`, `frontend/components/`, `frontend/tests/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T000 Create a new folder named 'Phase-II' and do all the working in it
- [x] T001 Create project structure with backend and frontend directories
- [x] T002 [P] Initialize Python project with FastAPI, SQLModel, and JWT verification dependencies in backend/
- [x] T003 [P] Initialize Next.js project with App Router in frontend/
- [x] T004 [P] Configure linting and formatting tools for both backend and frontend
- [x] T005 Set up project documentation files and README

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Set up database schema and migrations framework with SQLModel in backend/app/database/
- [x] T007 [P] Implement authentication/authorization framework with Better Auth in backend/app/auth/
- [x] T008 [P] Configure database models for User in backend/app/models/
- [x] T009 [P] Set up API routing and middleware structure in backend/app/api/
- [x] T010 Create base models/entities that all stories depend on
- [x] T011 Configure error handling and logging infrastructure in backend/app/utils/
- [x] T012 Setup environment configuration management in backend/app/config/
- [x] T013 [P] Create API client utilities in frontend/lib/api.ts
- [x] T014 [P] Set up authentication utilities in frontend/lib/auth.ts
- [x] T015 Create TypeScript type definitions in frontend/lib/types.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to register for an account using their email and password

**Independent Test**: Can be fully tested by navigating to the registration page, filling in user details, and verifying that a new user account is created and accessible.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [x] T016 [P] [US1] Contract test for POST /api/auth/register in backend/tests/contract/test_auth.py
- [x] T017 [P] [US1] Unit test for user registration service in backend/tests/unit/test_auth_service.py
- [x] T018 [P] [US1] Integration test for user registration flow in backend/tests/integration/test_auth.py

### Implementation for User Story 1

- [x] T019 [P] [US1] Create User model in backend/app/models/user.py
- [x] T020 [US1] Implement UserService in backend/app/services/user_service.py
- [x] T021 [US1] Implement registration endpoint in backend/app/api/v1/auth.py
- [x] T022 [US1] Add validation and error handling for registration
- [x] T023 [US1] Create registration schemas in backend/app/schemas/auth.py
- [x] T024 [US1] Create register page component in frontend/app/register/page.tsx
- [x] T025 [US1] Create registration form component in frontend/components/auth/RegisterForm.tsx

---

## Phase 4: User Story 2 - User Login (Priority: P1) 🎯 MVP

**Goal**: Enable registered users to log in to access their personal dashboard

**Independent Test**: Can be fully tested by navigating to the login page, entering valid credentials, and verifying that the user is authenticated and can access protected resources.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T026 [P] [US2] Contract test for POST /api/auth/login in backend/tests/contract/test_auth.py
- [x] T027 [P] [US2] Unit test for user login service in backend/tests/unit/test_auth_service.py
- [x] T028 [P] [US2] Integration test for user login flow in backend/tests/integration/test_auth.py

### Implementation for User Story 2

- [x] T029 [US2] Implement login endpoint in backend/app/api/v1/auth.py
- [x] T030 [US2] Implement JWT token generation in backend/app/services/auth_service.py
- [x] T031 [US2] Add validation and error handling for login
- [x] T032 [US2] Create login schemas in backend/app/schemas/auth.py
- [x] T033 [US2] Create login page component in frontend/app/login/page.tsx
- [x] T034 [US2] Create login form component in frontend/components/auth/LoginForm.tsx

---

## Phase 5: User Story 3 - JWT-based Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable session management via JWT tokens so users can securely access protected resources without repeatedly entering credentials

**Independent Test**: Can be fully tested by verifying that JWT tokens are properly issued on login, validated on protected endpoints, and expired appropriately.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T035 [P] [US3] Contract test for JWT token validation middleware in backend/tests/contract/test_auth_middleware.py
- [x] T036 [P] [US3] Unit test for JWT token validation in backend/tests/unit/test_jwt_utils.py
- [x] T037 [P] [US3] Integration test for protected endpoints in backend/tests/integration/test_protected_routes.py

### Implementation for User Story 3

- [x] T038 [US3] Implement JWT utilities in backend/app/utils/jwt.py
- [x] T039 [US3] Create authentication middleware in backend/app/middleware/auth.py
- [x] T040 [US3] Implement token refresh endpoint in backend/app/api/v1/auth.py
- [x] T041 [US3] Add token validation to protected endpoints
- [x] T042 [US3] Create JWT-related schemas in backend/app/schemas/auth.py

---

## Phase 6: User Story 4 - Protected Routes/Pages (Priority: P2)

**Goal**: Ensure that only authenticated users can access protected pages

**Independent Test**: Can be fully tested by attempting to access protected routes both when authenticated and when not authenticated, verifying appropriate access control.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [x] T043 [P] [US4] Unit test for protected route component in frontend/tests/auth/ProtectedRoute.test.tsx
- [x] T044 [P] [US4] Integration test for route protection in frontend/tests/integration/test_route_protection.tsx

### Implementation for User Story 4

- [x] T045 [US4] Create ProtectedRoute component in frontend/components/auth/ProtectedRoute.tsx
- [x] T046 [US4] Implement route protection logic in frontend/lib/auth/route-guard.ts
- [x] T047 [US4] Add protected routes to frontend/app/dashboard/page.tsx
- [x] T048 [US4] Configure frontend routing to use protection

---

## Phase 7: User Story 5 - Session Management (Priority: P3)

**Goal**: Enable users to securely end their session via logout functionality

**Independent Test**: Can be fully tested by logging in, clicking logout, and verifying that the session is terminated and the user can no longer access protected resources.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [x] T049 [P] [US5] Contract test for POST /api/auth/logout in backend/tests/contract/test_auth.py
- [x] T050 [P] [US5] Integration test for logout flow in backend/tests/integration/test_auth.py
- [x] T051 [P] [US5] Unit test for session invalidation in backend/tests/unit/test_session_service.py

### Implementation for User Story 5

- [x] T052 [US5] Implement logout endpoint in backend/app/api/v1/auth.py
- [x] T053 [US5] Implement session invalidation in backend/app/services/auth_service.py
- [x] T054 [US5] Create logout button component in frontend/components/auth/LogoutButton.tsx
- [x] T055 [US5] Add logout functionality to frontend navigation
- [x] T056 [US5] Implement token cleanup in frontend auth utilities