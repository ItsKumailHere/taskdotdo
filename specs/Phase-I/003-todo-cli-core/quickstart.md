# Quickstart: CLI Todo App Core Runtime

## Prerequisites
- Python 3.12+
- `uv` (modern Python package manager)

## Setup
1. Navigate to the project directory:
   ```bash
   cd phase-i-cli
   ```

2. Initialize the virtual environment and install dependencies:
   ```bash
   uv sync
   ```

## Development
To run the CLI application during development:
```bash
uv run todo --help
```

## Testing
Run the test suite using `pytest`:
```bash
uv run pytest
```

## CLI Usage Examples

### Add a task
```bash
uv run todo add "Buy milk" --priority high --tag personal
```

### List tasks
```bash
uv run todo list --priority high
```

### Toggle completion
```bash
uv run todo toggle <TASK_UUID>
```
