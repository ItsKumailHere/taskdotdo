# Research: Todo CRUD CLI

## Decisions

### CLI & UI Framework: Questionary + Rich
- **Decision**: Use `Questionary` for the interactive menu-driven loop and `Rich` for table/output formatting.
- **Rationale**:
    - `Questionary` provides an extremely simple API for creating interactive selection menus (`questionary.select(...)`), which perfectly aligns with the user's request for a "loop with prompted inputs".
    - `Rich` provides industry-standard terminal styling, tables, and colors, ensuring high UX marks for SC-004.
    - `Typer` is rejected for this specific interactive loop as it focuses on command arguments rather than conversational menu loops.

### Persistence: Pydantic + Atomic JSON Write
- **Decision**: Use `Pydantic` for serialization/deserialization and perform atomic writes to a local `todos.json` file on every collection change.
- **Rationale**:
    - `Pydantic` handles the complex task of validating sequential IDs and task status enums easily.
    - Atomic writes (writing to a temp file then renaming) prevent data corruption if the application is killed during a write operation.
    - Since the volume is low (<100 tasks), a single JSON file is the simplest viable solution (YAGNI).

### Package Management: uv
- **Decision**: Use `uv` for project management.
- **Rationale**: Mandated platform.

## Technical Context Updates

- **CLI Interface**: Interactive loop using `questionary`.
- **Formatting**: `Rich`.
- **Persistence**: `pydantic` models saved to `todos.json`.
- **Logic**: Service layer to manage ID generation and CRUD operations.
