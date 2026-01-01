# Research: CLI Todo App Core Runtime

## Decision 1: CLI Framework Selection

**Decision**: Use `typer`.

**Rationale**:
- Built on `click` but utilizes Python 3.12 type hints for automatic CLI schema definition.
- Extremely low boilerplate while providing robust validation and shell completion.
- Excellent IDE support and simpler command definitions compared to `argparse`.
- Aligns with the project's "Simplicity" and "Python 3.11+" principles.

**Alternatives Considered**:
- `argparse`: Rejected due to verbosity and lack of modern decorator patterns.
- `click`: Rejected in favor of `typer`'s superior type integration, despite `click` being the underlying engine.

---

## Decision 2: Architecture Pattern

**Decision**: Layered Service Pattern with Singleton Storage.

**Rationale**:
- **Service Layer**: Decouples business logic (task management) from the CLI presentation layer.
- **Singleton Pattern**: Ensures a consistent in-memory store is available throughout the CLI session lifetime.
- **Pydantic Models**: Provides robust validation (e.g., character limits) and automatic JSON serialization, which is a core requirement (default JSON output).
- **OOP Principles**: Models and Services will be implemented as classes with clear encapsulation.

**Alternatives Considered**:
- Functional-only approach: Rejected as user explicitly requested OOP principles.
- Active Record pattern: Rejected to keep entities (Pydantic models) separate from storage logic, making future persistence (Phase II) easier to implement.

---

## Decision 3: Project Management & Structure

**Decision**: `uv` with standard source layout.

**Rationale**:
- `uv` provides extremely fast environment management and modern `pyproject.toml` support.
- Standard layout (`src/todo/`) ensures compatibility with packaging tools and easier testing.
- Target directory: `phase-i-cli/` to isolate Phase 1 work as requested.

---

## Decision 4: Type Hinting & Python 3.12 Features

**Decision**: Utilize PEP 695 (type parameter syntax) and PEP 604 (union types).

**Rationale**:
- Keeps code concise and modern.
- `type TaskID = UUID` and `Task | None` are clearer than legacy `TypeVar` and `Optional`.
- Enhanced f-strings will simplify the creation of formatted JSON error messages.
