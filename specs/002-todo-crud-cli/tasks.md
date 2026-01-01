# Tasks: Todo CRUD CLI (Interactive)

**Input**: Design documents from `/specs/002-todo-crud-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as requested by the plan.md (using pytest).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths shown below assume structure from plan.md: `src/todo_cli/`, `tests/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T000 Create a new directory named 'todo-crud-cli' and build everything within it
- [x] T001 Initialize project directory structure per implementation plan
- [x] T002 Initialize `uv` project and add dependencies (typer, prompt_toolkit, rich, pydantic, pytest)
- [x] T003 [P] Configure `pyproject.toml` with `src` layout and scripts for `uv run todo_cli`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T004 [P] Define `Task` Pydantic model in `src/todo_cli/models.py`
- [x] T005 Create singleton `TodoRepository` in `src/todo_cli/repository.py` for in-memory storage
- [x] T006 [P] Implement shared UI formatting helpers (tables, panels) in `src/todo_cli/ui.py` using Rich
- [x] T007 Initialize Typer app and command routing in `src/todo_cli/commands.py`
- [x] T008 [P] Setup basic error handling and exception classes in `src/todo_cli/app.py`
- [x] T009 Implement the main interactive REPL loop logic in `src/todo_cli/app.py` using `prompt_toolkit`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Allow users to add tasks and see the list

**Independent Test**: Start app, run `add "Task 1"`, run `ls`, verify "Task 1" appears in table

### Tests for User Story 1

- [x] T010 [P] [US1] Unit test for repository `add` and `get_all` in `tests/test_repository.py`
- [x] T011 [US1] Functional test for `add` and `ls` commands in `tests/test_flow.py`

### Implementation for User Story 1

- [x] T012 [US1] Implement `add` command logic in `src/todo_cli/commands.py`
- [x] T013 [US1] Implement `ls` command logic with Rich table in `src/todo_cli/commands.py`
- [x] T014 [US1] Integrate `add` and `ls` into REPL loop in `src/todo_cli/app.py`
- [x] T015 [US1] Set newest-first ordering logic in `TodoRepository.get_all` in `src/todo_cli/repository.py`

**Checkpoint**: MVP Complete. Users can manage a basic list.

---

## Phase 4: User Story 2 - Complete and Delete Tasks (Priority: P2)

**Goal**: Mark tasks as done or remove them

**Independent Test**: Start app, `add "Task"`, verify ID, `done [ID]`, verify status, `rm [ID]`, verify gone from `ls`
  
### Tests for User Story 2

- [x] T016 [P] [US2] Unit test for repository `update_status` and `delete` in `tests/test_repository.py`
- [x] T017 [US2] Functional test for `done` and `rm` commands in `tests/test_flow.py`

### Implementation for User Story 2

- [x] T018 [US2] Implement `done` command in `src/todo_cli/commands.py`
- [x] T019 [US2] Implement `rm` command in `src/todo_cli/commands.py`
- [x] T020 [US2] Integrate `done` and `rm` into REPL loop in `src/todo_cli/app.py`
- [x] T021 [US2] Add non-existent ID error handling for `done` and `rm` in `src/todo_cli/commands.py`

**Checkpoint**: Core CRUD complete.

---

## Phase 5: User Story 3 - Update Task Descriptions (Priority: P3)

**Goal**: Edit existing task text

**Independent Test**: `add "Typo"`, `edit [ID] "Fixed"`, verify `ls` shows "Fixed"

### Tests for User Story 3

- [x] T022 [P] [US3] Unit test for repository `update_description` in `tests/test_repository.py`
- [x] T023 [US3] Functional test for `edit` command in `tests/test_flow.py`

### Implementation for User Story 3

- [x] T024 [US3] Implement `edit` command in `src/todo_cli/commands.py`
- [x] T025 [US3] Integrate `edit` into REPL loop in `src/todo_cli/app.py`

---

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T026 [P] Implement `exit` command and graceful shutdown in `src/todo_cli/app.py`
- [x] T027 [P] Add command history and basic autocomplete to `prompt_toolkit` loop in `src/todo_cli/app.py`
- [x] T028 Add "Help" command to display available REPL commands in `src/todo_cli/ui.py`
- [x] T029 Clean up Rich formatting for consistent "look and feel" in `src/todo_cli/ui.py`
- [x] T030 Final validation run against `quickstart.md` scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on T001-T003. BLOCKS all user stories.
- **User Stories (Phase 3+)**: Depend on Phase 2 completion.
  - US1 (P1) → US2 (P2) → US3 (P3) recommended for MVP flow.
- **Polish (Phase 6)**: Final wrapping.

### User Story Dependencies

- **US1 (P1)**: The anchor for the app.
- **US2/US3**: Depend on the data structure established in US1.

### Parallel Opportunities

- T004, T006, T008 can be developed in parallel with repo/loop setup.
- Once Foundation is done, US1-US3 implementation tasks are logically separate but share `commands.py` and `app.py`. Parallel work requires careful git merging or sequential implementation.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Complete US1 (Add/List).
3. **STOP and VALIDATE**: Verify the interactive loop starts and handles basic input.

### Incremental Delivery

1. Foundation ready.
2. US1 -> Verify MVP.
3. US2 -> Complete CRUD.
4. US3 -> Refine.
5. Polish -> UX improvements.
