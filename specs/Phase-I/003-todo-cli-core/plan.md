# Implementation Plan: CLI Todo App Core Runtime

**Branch**: `001-todo-cli-core` | **Date**: 2025-12-30 | **Spec**: [specs/001-todo-cli-core/spec.md](../001-todo-cli-core/spec.md)
**Input**: Feature specification from `/specs/001-todo-cli-core/spec.md`

## Summary

Build a foundational CLI-based todo application using Python 3.12 and OOP principles. The application will support in-memory storage of tasks and provide basic CRUD operations, filtering, and sorting, with structured JSON output as the default. All development versioning and environment management will be handled by `uv`.

## Technical Context

**Language/Version**: Python 3.12 (Mandatory)
**Primary Dependencies**: `uv`, `typer[all]`, `pydantic>=2.0`
**Storage**: In-memory (Singleton service with `dict[UUID, Task]`)
**Testing**: `pytest`, `pytest-cov`
**Target Platform**: Linux/macOS/Windows
**Project Type**: CLI Application
**Performance Goals**: <100ms for all in-memory operations
**Constraints**:
- Memory-only storage for Phase 1
- JSON-only structured output
- Maximum 255 chars for descriptions, 20 chars per tag
- All code must reside in `phase-i-cli/` directory
**Scale/Scope**: Single developer CLI app, up to 1000 tasks in memory

## Constitution Check

*GATE: Must pass before Phase 1 design.*

| Principle | Status | Confirmation |
|-----------|--------|--------------|
| I. Spec-First | PASS | Specification exists and is clarified. |
| II. AI-Generated | PASS | Code generation planned for implementation phase. |
| III. SSOT | PASS | Spec and plan are the authority. |
| IV. Phase Timing | PASS | Aligned with Phase I (In-Memory app). |
| V. Traceability | PASS | PHRs and PRs will track all decisions. |
| VI. Simplicity | PASS | Using `typer` to minimize boilerplate. |

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli-core/
├── plan.md              # This file
├── research.md          # Complete: Framework selection (typer), architecture
├── data-model.md        # Complete: Task entity, JSON contracts
├── quickstart.md        # Complete: Setup and dev instructions
├── contracts/
│   └── cli.md           # Complete: Command definitions
└── tasks.md             # To be created by /sp.tasks
```

### Source Code

All source resides in the `phase-i-cli/` directory.

```text
phase-i-cli/
├── pyproject.toml       # uv configuration
├── src/
│   └── todo/            # Main package
│       ├── __init__.py
│       ├── main.py      # Entry point (app = typer.Typer())
│       ├── models.py    # Pydantic Task and Response models
│       ├── services.py  # TaskService (Singleton)
│       └── cli.py       # Typer command logic
├── tests/
│   ├── unit/            # Service and model tests
│   └── integration/     # CLI execution tests via Typer's CliRunner
└── README.md            # User-facing summary
```

## Complexity Tracking

*No violations identified.*
