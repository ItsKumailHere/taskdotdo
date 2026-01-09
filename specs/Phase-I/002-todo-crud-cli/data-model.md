# Data Model: Todo CRUD CLI

## Entities

### Task

Represents a single work item in the todo list.

| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| `id` | `int` | Unique identifier | Primary Key, Sequential |
| `description` | `str` | Task content | Max 255 chars, Not Empty |
| `status` | `str` | Current state | Enum: ["Pending", "Completed"] |

## Relationships

- **Collection**: A flat list of `Task` objects stored in a JSON array.

## Validation Rules

1. **ID**: Must be positive and unique.
2. **Description**:
   - MUST be between 1 and 255 characters.
   - Whitespace handled (stripped).
3. **Status**:
   - Defaults to "Pending" on creation.
   - Transition: Any state to any allowed state.

## State Transitions

| From | To | Action |
|------|----|--------|
| - | Pending | Create |
| Pending | Completed | Mark Done |
| Completed | Pending | Mark Undone |
| Any | Deleted | Delete |
| Any | [Any] | Update Description |
