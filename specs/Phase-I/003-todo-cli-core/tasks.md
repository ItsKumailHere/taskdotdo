# Tasks: CLI Todo App Core Runtime

**Input**: Design documents from `/specs/001-todo-cli-core/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are explicitly requested in the implementation plan (using `pytest`).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths shown below are relative to `phase-i-cli/`
- All source files should be in `phase-i-cli/src/todo/`
- All test files should be in `phase-i-cli/tests/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Python 3.12 project with `uv` in `phase-i-cli/`
- [x] T002 Configure `pyproject.toml` with `typer[all]`, `pydantic>=2.0`, and `pytest`
- [x] T003 [P] Setup directory structure for `src/todo/` and `tests/` in `phase-i-cli/`
- [x] T004 [P] Create `.python-version` specifying 3.12 in `phase-i-cli/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Create `Task` and `Response` Pydantic models in `phase-i-cli/src/todo/models.py`
- [x] T006 Initialize `TaskService` singleton in `phase-i-cli/src/todo/services.py`
- [x] T007 Setup `Typer` app entry point in `phase-i-cli/src/todo/main.py`
- [x] T008 Configure base CLI output formatter for JSON in `phase-i-cli/src/todo/cli.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Discover and Launch CLI (Priority: P1) 🎯 MVP

**Goal**: Enable users to discover commands and launch the CLI with a single command.

**Independent Test**: Run `uv run todo --help` and verify help output.

### Tests for User Story 1
- [x] T009 [P] [US1] Create integration test for help command in `phase-i-cli/tests/integration/test_help.py`

### Implementation for User Story 1
- [x] T010 [US1] Implement version display in `phase-i-cli/src/todo/main.py`
- [x] T011 [US1] Configure script entry point in `pyproject.toml` so `uv run todo` works
- [x] T012 [US1] Add basic help descriptions to the Typer app in `phase-i-cli/src/todo/main.py`

**Checkpoint**: User Story 1 functional

---

## Phase 4: User Story 2 - Add New Tasks (Priority: P1)

**Goal**: Allow users to create new todo items with description, priority, and tags.

**Independent Test**: Run `uv run todo add "My Task"` and verify JSON output.

### Tests for User Story 2
- [x] T013 [P] [US2] Unit test for `TaskService.create` in `phase-i-cli/tests/unit/test_services.py`
- [x] T014 [P] [US2] Integration test for `add` command in `phase-i-cli/tests/integration/test_add.py`

### Implementation for User Story 2
- [x] T015 [US2] Implement `create` method in `phase-i-cli/src/todo/services.py` with UUID and timestamps
- [x] T016 [US2] Implement `add` command in `phase-i-cli/src/todo/cli.py`
- [x] T017 [US2] Implement description length and character validation in `phase-i-cli/src/todo/models.py` (max 255 chars)

**Checkpoint**: User Story 2 functional

---

## Phase 5: User Story 3 - View Task List (Priority: P1)

**Goal**: Display all tasks in structured JSON format.

**Independent Test**: Add a task then run `uv run todo list` and verify JSON array.

### Tests for User Story 3
- [x] T018 [P] [US3] Unit test for `TaskService.list_all` in `phase-i-cli/tests/unit/test_services.py`
- [x] T019 [P] [US3] Integration test for `list` command in `phase-i-cli/tests/integration/test_list.py`

### Implementation for User Story 3
- [x] T020 [US3] Implement `list_all` method in `phase-i-cli/src/todo/services.py`
- [x] T021 [US3] Implement `list` command in `phase-i-cli/src/todo/cli.py`

**Checkpoint**: User Story 3 functional

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Remove tasks from the list by identifier.

**Independent Test**: Run `uv run todo delete <UUID>` and verify task is gone.

### Tests for User Story 4
- [x] T022 [P] [US4] Unit test for `TaskService.delete` in `phase-i-cli/tests/unit/test_services.py`
- [x] T023 [P] [US4] Integration test for `delete` command in `phase-i-cli/tests/integration/test_delete.py`

### Implementation for User Story 4
- [x] T024 [US4] Implement `delete` method in `phase-i-cli/src/todo/services.py`
- [x] T025 [US4] Implement `delete` command in `phase-i-cli/src/todo/cli.py`

**Checkpoint**: User Story 4 functional

---

## Phase 7: User Story 5 - Update Task Details (Priority: P2)

**Goal**: Modify description, priority, or tags of an existing task.

**Independent Test**: Run `uv run todo update <UUID> --description "New"` and verify change.

### Tests for User Story 5
- [x] T026 [P] [US5] Unit test for `TaskService.update` in `phase-i-cli/tests/unit/test_services.py`
- [x] T027 [P] [US5] Integration test for `update` command in `phase-i-cli/tests/integration/test_update.py`

### Implementation for User Story 5
- [x] T028 [US5] Implement `update` method in `phase-i-cli/src/todo/services.py`
- [x] T029 [US5] Implement `update` command in `phase-i-cli/src/todo/cli.py`

**Checkpoint**: User Story 5 functional

---

## Phase 8: User Story 6 - Mark Task Complete (Priority: P2)

**Goal**: Toggle task completion status.

**Independent Test**: Run `uv run todo toggle <UUID>` and verify status changes.

### Tests for User Story 6
- [x] T030 [P] [US6] Unit test for `TaskService.toggle` in `phase-i-cli/tests/unit/test_services.py`
- [x] T031 [P] [US6] Integration test for `toggle` command in `phase-i-cli/tests/integration/test_toggle.py`

### Implementation for User Story 6
- [x] T032 [US6] Implement `toggle` method in `phase-i-cli/src/todo/services.py`
- [x] T033 [US6] Implement `toggle` command in `phase-i-cli/src/todo/cli.py`

**Checkpoint**: User Story 6 functional

---

## Phase 9: User Story 7 - Search and Filter Tasks (Priority: P3)

**Goal**: Filter by keyword, status, or priority.

**Independent Test**: Run `uv run todo list --search "milk"` and verify results.

### Tests for User Story 7
- [x] T034 [P] [US7] Unit test for filtering logic in `phase-i-cli/tests/unit/test_services.py`
- [x] T035 [P] [US7] Integration test for list filtering in `phase-i-cli/tests/integration/test_list_filter.py`

### Implementation for User Story 7
- [x] T036 [US7] Implement filtering parameters in `TaskService.list_all`
- [x] T037 [US7] Update `list` command in `phase-i-cli/src/todo/cli.py` to support filtering options

**Checkpoint**: User Story 7 functional

---

## Phase 10: User Story 8 - Sort Task List (Priority: P3)

**Goal**: Sort by date, priority, or alphabetically.

**Independent Test**: Run `uv run todo list --sort priority` and verify order.

### Tests for User Story 8
- [x] T038 [P] [US8] Unit test for sorting logic in `phase-i-cli/tests/unit/test_services.py`
- [x] T039 [P] [US8] Integration test for list sorting in `phase-i-cli/tests/integration/test_list_sort.py`

### Implementation for User Story 8
- [x] T040 [US8] Implement sorting logic in `TaskService.list_all`
- [x] T041 [US8] Update `list` command in `phase-i-cli/src/todo/cli.py` to support sorting options

**Checkpoint**: User Story 8 functional

---

## Phase 11: User Story 9 - Interactive Mode (Priority: P3)

**Goal**: Run the app continuously with a REPL-style interface, eliminating the need to repeatedly invoke commands.

**Independent Test**: Run uv run todo interactive and execute multiple commands in succession without exiting.
### Tests for User Story 9

- [x] T046 [P] [US9] Unit test for command parser in phase-i-cli/tests/unit/test_interactive.py
- [x] T047 [P] [US9] Integration test for interactive session lifecycle in phase-i-cli/tests/integration/test_interactive.py

### Implementation for User Story 9

- [x] T048 [US9] Create InteractiveSession class in phase-i-cli/src/todo/interactive.py with REPL loop
- [x] T049 [US9] Implement command parsing and routing to existing CLI commands in phase-i-cli/src/todo/interactive.py
- [x] T050 [US9] Add interactive command to phase-i-cli/src/todo/cli.py that launches the REPL
- [x] T051 [US9] Implement prompt with context (task count, filters) in phase-i-cli/src/todo/interactive.py
- [x] T052 [US9] Add exit, quit, and help commands specific to interactive mode
- [x] T053 [US9] Handle command history and readline support for better UX in phase-i-cli/src/todo/interactive.py

**Checkpoint**: User Story 9 functional

Phase 12: Polish & Cross-Cutting Concerns
Purpose: Final cleanup and validation

- [x] T054 [P] Create phase-i-cli/README.md with usage instructions (update to include interactive mode)
- [x] T055 Add detailed comments to all modules in phase-i-cli/src/todo/
- [x] T056 [P] Run all tests with coverage check: uv run pytest --cov=todo
- [x] T057 Final verification of JSON output structure across all commands

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup (Phase 1)
- **User Stories (Phases 3-10)**: All depend on Foundational (Phase 2)
- **Polish (Phase 11)**: Depends on completion of desired user stories

### User Story Execution Strategy

1. **MVP**: Complete US1 (T009-T012), US2 (T013-T017), and US3 (T018-T021).
2. **Core Features**: Complete US4, US5, US6 (T022-T033).
3. **Advanced Features**: Complete US7, US8 (T034-T041).

### Parallel Opportunities

- Tasks marked with **[P]** within the same phase can be executed in parallel.
- User stories can be implemented in parallel once Foundational (Phase 2) is complete.

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3)

1. Complete Phase 1 & 2.
2. Implement US1, US2, and US3.
3. Validate basic CLI lifecycle: Add task -> List tasks -> Help.

### Incremental Delivery

- Add US4 (Delete), US5 (Update), and US6 (Toggle) as next priority.
- Finally add US7 (Search/Filter) and US8 (Sort) to complete Phase 1 scope.
