# CLI Contract: Core Commands

## Global Options
- `--help`: Show usage and subcommand documentation.
- `--version`: Show application version.

## Commands

### `add`
Create a new task.

**Arguments**:
- `description` (str): Task description (1-255 chars).

**Options**:
- `--priority` (high|medium|low): Set task priority. Default: `medium`.
- `--tag` (str): Add tags (can be used multiple times).

**Output**: JSON representation of the created task.

---

### `list`
List all tasks.

**Options**:
- `--status` (complete|incomplete): Filter by status.
- `--priority` (high|medium|low): Filter by priority.
- `--search` (str): Keyword search in descriptions.
- `--sort` (date|priority|alpha): Sort the output.

**Output**: JSON array of matching tasks.

---

### `delete`
Remove a task.

**Arguments**:
- `task_id` (UUID): ID of the task to delete.

**Output**: JSON status confirmation.

---

### `update`
Modify an existing task.

**Arguments**:
- `task_id` (UUID): ID of the task to update.

**Options**:
- `--description` (str): New description.
- `--priority` (high|medium|low): New priority.
- `--tag` (str): New list of tags (replaces existing).

**Output**: JSON representation of the updated task.

---

### `toggle`
Toggle completion status.

**Arguments**:
- `task_id` (UUID): ID of the task.

**Output**: JSON representation of the task with new status.
