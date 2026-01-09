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

- **Web app**: `backend/`, `frontend/` at repository root
- **Backend**: `backend/app/`, `backend/tests/`
- **Frontend**: `frontend/app/`, `frontend/components/`, `frontend/tests/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with backend and frontend directories
- [X] T002 [P] Initialize Python project with FastAPI, SQLModel, and JWT verification dependencies in backend/
- [X] T003 [P] Initialize Next.js project with App Router in frontend/
- [X] T004 [P] Configure linting and formatting tools for both backend and frontend
- [X] T005 Set up project documentation files and README

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 [P] Set up database schema and migrations framework with SQLModel in backend/app/database/
- [X] T007 [P] Implement authentication/authorization framework with Better Auth in backend/app/auth/
- [X] T008 [P] Configure database models for User, Todo, Tag, Category, Notification, Session in backend/app/models/
- [X] T009 [P] Set up API routing and middleware structure in backend/app/api/
- [X] T010 Create base models/entities that all stories depend on
- [X] T011 Configure error handling and logging infrastructure in backend/app/utils/
- [X] T012 Setup environment configuration management in backend/app/config/
- [X] T013 [P] Create API client utilities in frontend/lib/api.ts
- [X] T014 [P] Set up authentication utilities in frontend/lib/auth.ts
- [X] T015 Create TypeScript type definitions in frontend/lib/types.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable new users to register for an account using their email and password, and returning users to log in to access their personal dashboard

**Independent Test**: Can be fully tested by registering a new user account and logging in successfully, delivering the ability to access the personal dashboard.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US1] Contract test for POST /api/auth/register in backend/tests/contract/test_auth.py
- [ ] T017 [P] [US1] Contract test for POST /api/auth/login in backend/tests/contract/test_auth.py
- [ ] T018 [P] [US1] Contract test for POST /api/auth/logout in backend/tests/contract/test_auth.py
- [ ] T019 [P] [US1] Integration test for user registration flow in backend/tests/integration/test_auth.py
- [ ] T020 [P] [US1] Integration test for user login flow in backend/tests/integration/test_auth.py
- [ ] T021 [P] [US1] Unit test for authentication service in backend/tests/unit/test_auth_service.py

### Implementation for User Story 1

- [X] T022 [P] [US1] Create User model in backend/app/models/user.py
- [X] T023 [P] [US1] Create Session model in backend/app/models/session.py
- [X] T024 [US1] Implement UserService in backend/app/services/user_service.py
- [X] T025 [US1] Implement AuthService in backend/app/services/auth_service.py
- [X] T026 [US1] Implement authentication endpoints in backend/app/api/v1/auth.py
- [X] T027 [US1] Implement user endpoints in backend/app/api/v1/users.py
- [X] T028 [US1] Add validation and error handling for authentication
- [X] T029 [US1] Create authentication schemas in backend/app/schemas/auth.py
- [X] T030 [US1] Create user schemas in backend/app/schemas/user.py
- [X] T031 [US1] Create login page component in frontend/app/login/page.tsx
- [X] T032 [US1] Create register page component in frontend/app/register/page.tsx
- [X] T033 [US1] Create dashboard page component in frontend/app/dashboard/page.tsx
- [X] T034 [US1] Create authentication form component in frontend/components/AuthForm.tsx
- [X] T035 [US1] Implement authentication utilities in frontend/lib/auth.ts
- [X] T036 [US1] Add protected route middleware in frontend/middleware.ts
- [X] T037 [US1] Add navigation component with login/logout in frontend/components/Navbar.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Todo Management (Priority: P1)

**Goal**: Enable users to create, view, edit, mark complete/incomplete, and delete their todos with descriptions, due dates, tags, and categories

**Independent Test**: Can be fully tested by creating, viewing, updating, and deleting todos, delivering the core task management capability.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T038 [P] [US2] Contract test for GET /api/todos in backend/tests/contract/test_todos.py
- [ ] T039 [P] [US2] Contract test for POST /api/todos in backend/tests/contract/test_todos.py
- [ ] T040 [P] [US2] Contract test for GET /api/todos/{id} in backend/tests/contract/test_todos.py
- [ ] T041 [P] [US2] Contract test for PUT /api/todos/{id} in backend/tests/contract/test_todos.py
- [ ] T042 [P] [US2] Contract test for DELETE /api/todos/{id} in backend/tests/contract/test_todos.py
- [ ] T043 [P] [US2] Integration test for todo CRUD operations in backend/tests/integration/test_todos.py
- [ ] T044 [P] [US2] Unit test for todo service in backend/tests/unit/test_todo_service.py

### Implementation for User Story 2

- [X] T045 [P] [US2] Create Todo model in backend/app/models/todo.py
- [X] T046 [P] [US2] Create TodoTag model in backend/app/models/todo_tag.py
- [X] T047 [P] [US2] Create Notification model in backend/app/models/notification.py
- [X] T048 [US2] Implement TodoService in backend/app/services/todo_service.py
- [X] T049 [US2] Implement NotificationService in backend/app/services/notification_service.py
- [X] T050 [US2] Implement todo endpoints in backend/app/api/v1/todos.py
- [X] T051 [US2] Implement notification endpoints in backend/app/api/v1/notifications.py
- [X] T052 [US2] Add validation and error handling for todo operations
- [X] T053 [US2] Create todo schemas in backend/app/schemas/todo.py
- [X] T054 [US2] Create notification schemas in backend/app/schemas/notification.py
- [X] T055 [US2] Create TodoItem component in frontend/components/TodoItem.tsx
- [X] T056 [US2] Create TodoList component in frontend/components/TodoList.tsx
- [X] T057 [US2] Create TodoForm component in frontend/components/TodoForm.tsx
- [X] T058 [US2] Create todos page in frontend/app/todos/page.tsx
- [X] T059 [US2] Implement todo API functions in frontend/lib/api.ts
- [X] T060 [US2] Integrate with User Story 1 authentication components

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Todo Organization and Filtering (Priority: P2)

**Goal**: Enable users to organize their todos by filtering and sorting with tags, categories, and due dates

**Independent Test**: Can be fully tested by creating todos with various tags, categories, and due dates, then filtering and sorting them, delivering improved organization capabilities.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T061 [P] [US3] Contract test for GET /api/categories in backend/tests/contract/test_categories.py
- [ ] T062 [P] [US3] Contract test for POST /api/categories in backend/tests/contract/test_categories.py
- [ ] T063 [P] [US3] Contract test for GET /api/tags in backend/tests/contract/test_tags.py
- [ ] T064 [P] [US3] Contract test for POST /api/tags in backend/tests/contract/test_tags.py
- [ ] T065 [P] [US3] Integration test for todo organization features in backend/tests/integration/test_organization.py
- [ ] T066 [P] [US3] Unit test for category and tag services in backend/tests/unit/test_category_tag_service.py

### Implementation for User Story 3

- [X] T067 [P] [US3] Create Category model in backend/app/models/category.py
- [X] T068 [P] [US3] Create Tag model in backend/app/models/tag.py
- [X] T069 [US3] Implement CategoryService in backend/app/services/category_service.py
- [X] T070 [US3] Implement TagService in backend/app/services/tag_service.py
- [X] T071 [US3] Implement category endpoints in backend/app/api/v1/categories.py
- [X] T072 [US3] Implement tag endpoints in backend/app/api/v1/tags.py
- [X] T073 [US3] Add validation and error handling for organization features
- [X] T074 [US3] Create category schemas in backend/app/schemas/category.py
- [X] T075 [US3] Create tag schemas in backend/app/schemas/tag.py
- [X] T076 [US3] Create category management in frontend/components/CategoryManager.tsx
- [X] T077 [US3] Create tag management in frontend/components/TagManager.tsx
- [X] T078 [US3] Enhance TodoList component with filtering and sorting in frontend/components/TodoList.tsx
- [X] T079 [US3] Add category and tag API functions in frontend/lib/api.ts
- [X] T080 [US3] Integrate with User Story 1 and 2 components

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - User Experience Customization (Priority: P2)

**Goal**: Enable users to customize their UI experience with dark mode and themes, and receive browser-based notifications for upcoming due dates and reminders

**Independent Test**: Can be fully tested by switching between themes and receiving notifications, delivering improved user experience.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T081 [P] [US4] Contract test for PUT /api/users/me/preferences in backend/tests/contract/test_user_preferences.py
- [ ] T082 [P] [US4] Integration test for theme customization in frontend/tests/integration/test_theme.js
- [ ] T083 [P] [US4] Unit test for notification service in backend/tests/unit/test_notification_service.py

### Implementation for User Story 4

- [X] T084 [P] [US4] Update User model with preferences field in backend/app/models/user.py
- [X] T085 [US4] Implement user preference update endpoint in backend/app/api/v1/users.py
- [X] T086 [US4] Implement notification scheduling logic in backend/app/services/notification_service.py
- [X] T087 [US4] Create notification endpoints in backend/app/api/v1/notifications.py
- [X] T088 [US4] Add validation and error handling for preferences and notifications
- [X] T089 [US4] Create ThemeToggle component in frontend/components/ThemeToggle.tsx
- [X] T090 [US4] Implement dark mode functionality with Tailwind CSS in frontend/styles/globals.css
- [X] T091 [US4] Create notification system with browser notifications in frontend/components/NotificationSystem.tsx
- [X] T092 [US4] Update user preferences API functions in frontend/lib/api.ts
- [X] T093 [US4] Integrate with User Story 1, 2, and 3 components

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Session Management (Priority: P3)

**Goal**: Implement persistent sessions for up to 90 days and single-device login restriction

**Independent Test**: Can be fully tested by logging in, closing the browser/device, and returning within 90 days, delivering persistent access without re-authentication.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T094 [P] [US5] Unit test for session management in backend/tests/unit/test_session_service.py
- [ ] T095 [P] [US5] Integration test for session persistence in backend/tests/integration/test_session.py
- [ ] T096 [P] [US5] Integration test for single-device restriction in backend/tests/integration/test_session.py

### Implementation for User Story 5

- [X] T097 [P] [US5] Implement SessionService in backend/app/services/session_service.py
- [X] T098 [US5] Update authentication middleware to handle session management in backend/app/middleware/auth.py
- [X] T099 [US5] Implement session validation and cleanup logic in backend/app/services/session_service.py
- [X] T100 [US5] Add session-related endpoints in backend/app/api/v1/auth.py
- [X] T101 [US5] Add validation and error handling for session management
- [X] T102 [US5] Update authentication utilities to handle persistent sessions in frontend/lib/auth.ts
- [X] T103 [US5] Integrate with User Story 1 authentication components

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T104 [P] Documentation updates in docs/ and project root
- [X] T105 Code cleanup and refactoring
- [X] T106 Performance optimization across all stories
- [X] T107 [P] Additional unit tests (if requested) in backend/tests/unit/ and frontend/tests/unit/
- [X] T108 Security hardening
- [X] T109 Run quickstart.md validation
- [X] T110 Implement comprehensive error handling and user feedback
- [X] T111 Add input validation and sanitization
- [X] T112 Implement rate limiting for API endpoints
- [X] T113 Add comprehensive logging for debugging and monitoring
- [X] T114 Create deployment configuration files
- [X] T115 Set up automated testing pipeline

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for authentication
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 and US2 for user context and todos
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on US1 for user preferences
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Depends on US1 for authentication

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
Task: "Contract test for POST /api/auth/register in backend/tests/contract/test_auth.py"
Task: "Contract test for POST /api/auth/login in backend/tests/contract/test_auth.py"
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