# Tasks: Multi-User Todo Application

**Input**: Design documents from `/specs/001-multi-user-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below assume web app structure based on plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T000 Create a new directory and continue with the rest of the tasks within it
- [x] T001 Create project structure with backend and frontend directories
- [x] T002 Initialize Python project with FastAPI, SQLModel, Neon Postgres dependencies in backend
- [x] T003 [P] Initialize Next.js project with TypeScript in frontend
- [x] T004 [P] Configure linting and formatting tools for both backend and frontend
- [x] T005 Set up environment configuration management for both backend and frontend
- [x] T006 Configure project repository with proper gitignore and documentation files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Setup database schema and migrations framework using SQLModel in backend/app/database/
- [X] T008 [P] Implement authentication/authorization framework with JWT and Better Auth in backend/app/auth/
- [X] T009 [P] Setup API routing and middleware structure in backend/app/api/
- [X] T010 Create base models/entities that all stories depend on in backend/app/models/
- [X] T011 Configure error handling and logging infrastructure in backend/app/utils/
- [X] T012 Setup database connection pooling and session management in backend/app/database/
- [X] T013 [P] Create API client utilities for frontend in frontend/lib/api.ts
- [X] T014 [P] Set up authentication utilities for frontend in frontend/lib/auth.ts
- [X] T015 Create TypeScript type definitions for frontend in frontend/lib/types.ts

Output a clear and precise guide for the user to setup things as api keys and database outside of code 

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable new users to register for an account using their email and password, and returning users to log in to access their personal dashboard

**Independent Test**: Can be fully tested by registering a new user account and logging in successfully, delivering the ability to access the personal dashboard

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US1] Contract test for /api/auth/register endpoint in backend/tests/contract/test_auth.py
- [ ] T017 [P] [US1] Contract test for /api/auth/login endpoint in backend/tests/contract/test_auth.py
- [ ] T018 [P] [US1] Contract test for /api/auth/logout endpoint in backend/tests/contract/test_auth.py
- [ ] T019 [P] [US1] Integration test for user registration flow in backend/tests/integration/test_auth.py

### Implementation for User Story 1

- [ ] T020 [P] [US1] Create User model in backend/app/models/user.py
- [ ] T021 [P] [US1] Create Session model in backend/app/models/session.py
- [ ] T022 [US1] Implement UserService in backend/app/services/user_service.py
- [ ] T023 [US1] Implement AuthService in backend/app/services/auth_service.py
- [ ] T024 [US1] Implement authentication endpoints in backend/app/api/v1/auth.py
- [ ] T025 [US1] Create Pydantic schemas for auth in backend/app/schemas/auth.py
- [ ] T026 [US1] Create authentication utilities in backend/app/utils/auth.py
- [ ] T027 [US1] Implement session management logic in backend/app/services/session_service.py
- [ ] T028 [US1] Create registration page component in frontend/app/register/page.tsx
- [ ] T029 [US1] Create login page component in frontend/app/login/page.tsx
- [ ] T030 [US1] Create authentication form component in frontend/components/AuthForm.tsx
- [ ] T031 [US1] Implement authentication context in frontend/contexts/AuthContext.tsx
- [ ] T032 [US1] Add protected route handling in frontend/components/ProtectedRoute.tsx
- [ ] T033 [US1] Create dashboard page component in frontend/app/dashboard/page.tsx
- [ ] T034 [US1] Add validation and error handling for auth forms
- [ ] T035 [US1] Add logging for authentication operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Todo Management (Priority: P1)

**Goal**: Enable users to create, view, edit, mark complete/incomplete, and delete their todos with descriptions, due dates, tags, and categories

**Independent Test**: Can be fully tested by creating, viewing, updating, and deleting todos, delivering the core task management capability

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T036 [P] [US2] Contract test for /api/todos endpoints in backend/tests/contract/test_todos.py
- [ ] T037 [P] [US2] Integration test for todo CRUD operations in backend/tests/integration/test_todos.py

### Implementation for User Story 2

- [ ] T038 [P] [US2] Create Todo model in backend/app/models/todo.py
- [ ] T039 [P] [US2] Create Tag model in backend/app/models/tag.py
- [ ] T040 [P] [US2] Create Category model in backend/app/models/category.py
- [ ] T041 [P] [US2] Create TodoTag junction model in backend/app/models/todo_tag.py
- [ ] T042 [US2] Implement TodoService in backend/app/services/todo_service.py
- [ ] T043 [US2] Implement TagService in backend/app/services/tag_service.py
- [ ] T044 [US2] Implement CategoryService in backend/app/services/category_service.py
- [ ] T045 [US2] Implement todo endpoints in backend/app/api/v1/todos.py
- [ ] T046 [US2] Implement category endpoints in backend/app/api/v1/categories.py
- [ ] T047 [US2] Implement tag endpoints in backend/app/api/v1/tags.py
- [ ] T048 [US2] Create Pydantic schemas for todos in backend/app/schemas/todo.py
- [ ] T049 [US2] Create Pydantic schemas for categories in backend/app/schemas/category.py
- [ ] T050 [US2] Create Pydantic schemas for tags in backend/app/schemas/tag.py
- [ ] T051 [US2] Create TodoItem component in frontend/components/TodoItem.tsx
- [ ] T052 [US2] Create TodoList component in frontend/components/TodoList.tsx
- [ ] T053 [US2] Create TodoForm component in frontend/components/TodoForm.tsx
- [ ] T054 [US2] Create todos page in frontend/app/todos/page.tsx
- [ ] T055 [US2] Create todo detail page in frontend/app/todos/[id]/page.tsx
- [ ] T056 [US2] Implement todo CRUD operations in frontend/lib/api.ts
- [ ] T057 [US2] Add validation and error handling for todo operations
- [ ] T058 [US2] Integrate with User Story 1 components (user authentication)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Todo Organization and Filtering (Priority: P2)

**Goal**: Enable users to organize their todos by filtering and sorting with tags, categories, and due dates

**Independent Test**: Can be fully tested by creating todos with various tags, categories, and due dates, then filtering and sorting them, delivering improved organization capabilities

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T059 [P] [US3] Contract test for filtering and sorting parameters in /api/todos endpoint in backend/tests/contract/test_todos.py
- [ ] T060 [P] [US3] Integration test for filtering and sorting functionality in backend/tests/integration/test_todos.py

### Implementation for User Story 3

- [ ] T061 [P] [US3] Enhance TodoService with filtering and sorting methods in backend/app/services/todo_service.py
- [ ] T062 [US3] Update todo endpoints with filtering and sorting capabilities in backend/app/api/v1/todos.py
- [ ] T063 [US3] Add filtering and sorting parameters to todo schemas in backend/app/schemas/todo.py
- [ ] T064 [US3] Create filtering UI components in frontend/components/TodoFilters.tsx
- [ ] T065 [US3] Enhance TodoList component with filtering and sorting in frontend/components/TodoList.tsx
- [ ] T066 [US3] Add filtering and sorting functionality to frontend/lib/api.ts
- [ ] T067 [US3] Add validation and error handling for filtering operations
- [ ] T068 [US3] Integrate with User Story 1 and 2 components

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - User Experience Customization (Priority: P2)

**Goal**: Enable users to customize their UI experience with dark mode and themes, and receive browser-based notifications for upcoming due dates and reminders

**Independent Test**: Can be fully tested by switching between themes and receiving notifications, delivering improved user experience

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T069 [P] [US4] Contract test for /api/users/me/preferences endpoint in backend/tests/contract/test_users.py
- [ ] T070 [P] [US4] Integration test for theme customization in frontend/tests/integration/test_theme.ts

### Implementation for User Story 4

- [ ] T071 [P] [US4] Update User model with preferences field in backend/app/models/user.py
- [ ] T072 [US4] Implement user preferences endpoint in backend/app/api/v1/users.py
- [ ] T073 [US4] Create Notification model in backend/app/models/notification.py
- [ ] T074 [US4] Implement NotificationService in backend/app/services/notification_service.py
- [ ] T075 [US4] Create notification endpoints in backend/app/api/v1/notifications.py
- [ ] T076 [US4] Create ThemeToggle component in frontend/components/ThemeToggle.tsx
- [ ] T077 [US4] Implement theme context in frontend/contexts/ThemeContext.tsx
- [ ] T078 [US4] Add theme switching functionality to frontend/lib/theme.ts
- [ ] T079 [US4] Create notification system in frontend/lib/notifications.ts
- [ ] T080 [US4] Implement browser notifications for due dates in frontend/services/notificationService.ts
- [ ] T081 [US4] Add theme support to global styles in frontend/styles/globals.css
- [ ] T082 [US4] Integrate with User Story 1 components for user preferences
- [ ] T083 [US4] Add validation and error handling for theme operations

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Session Management (Priority: P3)

**Goal**: Implement user sessions that persist across device and browser restarts for up to 90 days, with single-device login restriction

**Independent Test**: Can be fully tested by logging in, closing the browser/device, and returning within 90 days, delivering persistent access without re-authentication

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T084 [P] [US5] Integration test for session persistence in backend/tests/integration/test_sessions.py
- [ ] T085 [P] [US5] Integration test for single-device restriction in backend/tests/integration/test_sessions.py

### Implementation for User Story 5

- [ ] T086 [US5] Enhance Session model with device fingerprinting in backend/app/models/session.py
- [ ] T087 [US5] Implement session validation and cleanup logic in backend/app/services/session_service.py
- [ ] T088 [US5] Add session middleware for single-device restriction in backend/app/middleware/session.py
- [ ] T089 [US5] Update authentication middleware to handle session management in backend/app/middleware/auth.py
- [ ] T090 [US5] Implement device fingerprinting in frontend/utils/deviceFingerprint.ts
- [ ] T091 [US5] Add session management to frontend authentication utilities in frontend/lib/auth.ts
- [ ] T092 [US5] Add validation and error handling for session operations
- [ ] T093 [US5] Integrate with User Story 1 components

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T094 [P] Documentation updates in docs/
- [ ] T095 Code cleanup and refactoring
- [ ] T096 Performance optimization across all stories
- [ ] T097 [P] Additional unit tests (if requested) in backend/tests/unit/ and frontend/tests/unit/
- [ ] T098 Security hardening
- [ ] T099 Run quickstart.md validation
- [ ] T100 UI/UX improvements and responsive design enhancements
- [ ] T101 Error boundary implementation in frontend
- [ ] T102 Input validation and sanitization across all endpoints
- [ ] T103 Database indexing for performance optimization
- [ ] T104 API rate limiting implementation
- [ ] T105 Frontend caching strategies implementation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Depends on US1 (authentication)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on US2 (todos exist to organize)
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (user preferences) and US2 (todos for notifications)
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 (authentication foundation)

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for /api/auth/register endpoint in backend/tests/contract/test_auth.py"
Task: "Contract test for /api/auth/login endpoint in backend/tests/contract/test_auth.py"
Task: "Contract test for /api/auth/logout endpoint in backend/tests/contract/test_auth.py"
Task: "Integration test for user registration flow in backend/tests/integration/test_auth.py"

# Launch all models for User Story 1 together:
Task: "Create User model in backend/app/models/user.py"
Task: "Create Session model in backend/app/models/session.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence