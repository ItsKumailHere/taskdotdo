# Quickstart: Todo CRUD CLI (Phase I)

## Setup

1. Ensure `uv` is installed.
2. Initialize project and sync dependencies:
   ```bash
   uv sync
   ```

## Usage

Start the interactive CLI session:
```bash
uv run -m todo_cli
```

### Interactive Menu
The application will prompt you with a selection menu:
- **Add Task**: Prompts for a description (max 255 chars).
- **List Tasks**: Shows all tasks in a formatted table.
- **Update Task**: Prompts for an ID and then a new description.
- **Complete Task**: Prompts for an ID to mark as "Completed".
- **Delete Task**: Prompts for an ID to remove.
- **Exit**: Saves data to `todos.json` and quits.

## Data Storage
Your tasks are saved locally in `./todos.json`.

## Running Tests
```bash
uv run pytest
```
