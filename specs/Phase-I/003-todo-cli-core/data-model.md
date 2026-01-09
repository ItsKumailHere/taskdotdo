# Data Model: CLI Todo App Core Runtime

## Entities

### Task

The core entity representing a todo item.

| Field | Type | Validation / Constraints | Default |
|-------|------|--------------------------|---------|
| `id` | `UUID` | Version 4 UUID | `uuid4()` |
| `description` | `str` | 1-255 characters, non-empty | Required |
| `status` | `Literal["complete", "incomplete"]` | Must be one of these | `"incomplete"` |
| `priority` | `Literal["high", "medium", "low"]` | Must be one of these | `"medium"` |
| `tags` | `list[str]` | Max 20 chars per tag | `[]` |
| `created_at` | `datetime` | ISO 8601 | `now()` |
| `updated_at` | `datetime` | ISO 8601 | `now()` |
| `due_date` | `datetime | None` | ISO 8601 | `None` |

## Business Logic / Service Rules

### Uniqueness
- Every task MUST have a globally unique UUID.

### Validation
- **Description**: Must be between 1 and 255 characters. Whitespace-only descriptions are rejected.
- **Tags**: Each tag must be 1-20 characters.

### State Transitions
- **Mark Complete**: Status changes to `"complete"`, `updated_at` is refreshed.
- **Unmark Complete**: Status changes to `"incomplete"`, `updated_at` is refreshed.

### Retention
- For Phase 1, data is held in-memory in a `dict[UUID, Task]` within the `TaskService` singleton.

## CLI Response Contract (JSON)

Every successful operation returns a JSON object with:
- `data`: The result (Task object, List of Tasks, or Status message)
- `metadata`: Execution details (status code, timestamp)

### Successful Resource (e.g., Get/Add/Update)
```json
{
  "data": {
    "id": "a96f764...",
    "description": "Buy milk",
    "status": "incomplete",
    "priority": "medium",
    "tags": ["personal"],
    "created_at": "2025-12-30T12:00:00Z",
    "updated_at": "2025-12-30T12:00:00Z"
  },
  "metadata": {
    "status": 200,
    "timestamp": "2025-12-30T12:00:01Z"
  }
}
```

### Error Response
```json
{
  "error": "Tasks cannot be created without descriptions",
  "metadata": {
    "status": 400,
    "timestamp": "2025-12-30T12:00:01Z"
  }
}
```
