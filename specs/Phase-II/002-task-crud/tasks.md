# Tasks: Task CRUD Operations

**Input**: Design documents from `/specs/Phase-II/002-task-crud/`
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

- [x] T100 [P] Create database model for Todo in backend/app/models/todo.py
- [x] T101 [P] Create schemas for Todo operations in backend/app/schemas/todo.py
- [x] T102 [P] Set up API routing structure for todos in backend/app/api/v1/todos.py
- [x] T103 [P] Create service layer for Todo operations in backend/app/services/todo_service.py
- [x] T104 [P] Create TypeScript type definitions for Todo in frontend/lib/types/todo.ts
- [x] T105 [P] Create API client utilities for Todo in frontend/lib/api/todo-api.ts

---

## Phase 2: User Story 1 - Create New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create new tasks

**Independent Test**: Can be fully tested by logging in, navigating to the task creation interface, filling in task details, and verifying that the new task appears in the user's task list.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [x] T106 [P] [US1] Contract test for POST /api/v1/todos in backend/tests/contract/test_todos.py
- [x] T107 [P] [US1] Unit test for task creation service in backend/tests/unit/test_todo_service.py
- [x] T108 [P] [US1] Integration test for task creation flow in backend/tests/integration/test_todos.py

### Implementation for User Story 1

- [x] T109 [US1] Implement create task endpoint in backend/app/api/v1/todos.py
- [x] T110 [US1] Implement task creation service in backend/app/services/todo_service.py
- [x] T111 [US1] Add validation and error handling for task creation
- [x] T112 [US1] Create task form component in frontend/components/tasks/TaskForm.tsx
- [x] T113 [US1] Add task creation functionality to dashboard in frontend/app/dashboard/page.tsx

---

## Phase 3: User Story 2 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to view all their tasks

**Independent Test**: Can be fully tested by logging in and verifying that all tasks associated with the user are displayed in the task list view.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T114 [P] [US2] Contract test for GET /api/v1/todos in backend/tests/contract/test_todos.py
- [x] T115 [P] [US2] Unit test for task retrieval service in backend/tests/unit/test_todo_service.py
- [x] T116 [P] [US2] Integration test for task retrieval flow in backend/tests/integration/test_todos.py

### Implementation for User Story 2

- [x] T117 [US2] Implement get tasks endpoint in backend/app/api/v1/todos.py
- [x] T118 [US2] Implement task retrieval service in backend/app/services/todo_service.py
- [x] T119 [US2] Add filtering and pagination to task retrieval
- [x] T120 [US2] Create task list component in frontend/components/tasks/TaskList.tsx
- [x] T121 [US2] Display tasks on dashboard in frontend/app/dashboard/page.tsx

---

## Phase 4: User Story 3 - Update Existing Tasks (Priority: P2)

**Goal**: Enable authenticated users to update their existing tasks

**Independent Test**: Can be fully tested by selecting an existing task, modifying its details, saving the changes, and verifying that the updated information is reflected in the task list.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T122 [P] [US3] Contract test for PUT /api/v1/todos/{id} in backend/tests/contract/test_todos.py
- [x] T123 [P] [US3] Unit test for task update service in backend/tests/unit/test_todo_service.py
- [x] T124 [P] [US3] Integration test for task update flow in backend/tests/integration/test_todos.py

### Implementation for User Story 3

- [x] T125 [US3] Implement update task endpoint in backend/app/api/v1/todos.py
- [x] T126 [US3] Implement task update service in backend/app/services/todo_service.py
- [x] T127 [US3] Add validation and error handling for task updates
- [x] T128 [US3] Enhance task form component for editing in frontend/components/tasks/TaskForm.tsx
- [x] T129 [US3] Add task editing functionality to task list in frontend/components/tasks/TaskList.tsx

---

## Phase 5: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Enable authenticated users to delete tasks that are no longer needed

**Independent Test**: Can be fully tested by selecting a task for deletion, confirming the action, and verifying that the task is removed from the task list.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [x] T130 [P] [US4] Contract test for DELETE /api/v1/todos/{id} in backend/tests/contract/test_todos.py
- [x] T131 [P] [US4] Unit test for task deletion service in backend/tests/unit/test_todo_service.py
- [x] T132 [P] [US4] Integration test for task deletion flow in backend/tests/integration/test_todos.py

### Implementation for User Story 4

- [x] T133 [US4] Implement delete task endpoint in backend/app/api/v1/todos.py
- [x] T134 [US4] Implement task deletion service in backend/app/services/todo_service.py
- [x] T135 [US4] Add confirmation and error handling for task deletion
- [x] T136 [US4] Create delete confirmation dialog in frontend/components/tasks/DeleteConfirmation.tsx
- [x] T137 [US4] Add delete functionality to task list in frontend/components/tasks/TaskList.tsx

---

## Phase 6: User Story 5 - Mark Tasks Complete/Incomplete (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to mark tasks as complete or incomplete

**Independent Test**: Can be fully tested by selecting a task and toggling its completion status, then verifying that the status change is reflected in the task list and persisted.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [x] T138 [P] [US5] Contract test for PATCH /api/v1/todos/{id}/status in backend/tests/contract/test_todos.py
- [x] T139 [P] [US5] Unit test for task status update service in backend/tests/unit/test_todo_service.py
- [x] T140 [P] [US5] Integration test for task status update flow in backend/tests/integration/test_todos.py

### Implementation for User Story 5

- [x] T141 [US5] Implement update task status endpoint in backend/app/api/v1/todos.py
- [x] T142 [US5] Implement task status update service in backend/app/services/todo_service.py
- [x] T143 [US5] Add validation and error handling for status updates
- [x] T144 [US5] Create status toggle component in frontend/components/tasks/StatusToggle.tsx
- [x] T145 [US5] Add status toggle functionality to task list in frontend/components/tasks/TaskList.tsx

---

## Phase 7: Task Management Features (Priority: P2)

**Goal**: Implement advanced task management features including filtering, sorting, and search

### Implementation for Task Management

- [x] T146 [P] Implement task filtering by status in backend/app/api/v1/todos.py
- [x] T147 [P] Implement task sorting by various fields in backend/app/api/v1/todos.py
- [x] T148 [P] Create filter and sort controls in frontend/components/tasks/TaskFilters.tsx
- [x] T149 [P] Add search functionality to task list in frontend/components/tasks/TaskList.tsx
- [x] T150 [P] Update dashboard to include task statistics in frontend/app/dashboard/page.tsx`