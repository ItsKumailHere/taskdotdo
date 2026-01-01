# CLI Interface Contract: Todo CRUD CLI

## Interactive Mode
The application MUST start into a persistent REPL session.

### `exit`
Exit the application.
- **Output**: Farewell message.

### `add`
Add a new task.
- **Usage**: `add "description"`
- **Output**: Success feedback with Task ID.

### `ls`
List tasks.
- **Usage**: `ls` or `ls --status Completed`
- **Output**: Rich-formatted table, ordered newest first.

### `done`
Mark a task as completed.
- **Usage**: `done [id]`
- **Output**: Checkmark feedback.

### `edit`
Update task description.
- **Usage**: `edit [id] "new description"`
- **Output**: Update confirmation.

### `rm`
Delete a task.
- **Usage**: `rm [id]`
- **Output**: Deletion confirmation.

## Error Schema

| Code | Message | Scenario |
|------|---------|----------|
| UNKNOWN_COMMAND | Error: Unknown command '{cmd}'. Type 'help' for options. | Input not in command list. |
| NOT_FOUND | Error: Task with ID {id} not found. | ID missing in current session. |
| VALIDATION_ERROR | Error: {field} must be {rule}. | Pydantic validation failure. |
