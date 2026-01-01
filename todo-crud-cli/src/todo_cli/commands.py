# Typer command routing
import typer
from .repository import TodoRepository
from .ui import display_tasks, show_message, show_error
from .models import TaskStatus
from typing import Optional

cli = typer.Typer(add_completion=False, pretty_exceptions_enable=False)
repo = TodoRepository()

@cli.command(name="add")
def add(description: str):
    """Add a new task."""
    task = repo.add_task(description)
    show_message(f"Task added successfully! (ID: {task.id})")

@cli.command(name="ls")
def ls(status: Optional[TaskStatus] = typer.Option(None, help="Filter by status")):
    """List all tasks."""
    tasks = repo.get_all_tasks(status)
    display_tasks(tasks)

@cli.command(name="done")
def done(task_id: int):
    """Mark a task as completed."""
    task = repo.update_task_status(task_id, TaskStatus.COMPLETED)
    if task:
        show_message(f"Task {task_id} marked as completed.", style="green")
    else:
        show_error(f"Task with ID {task_id} not found.")
        raise typer.Exit(code=1)

@cli.command(name="edit")
def edit(task_id: int, description: str):
    """Update task description."""
    task = repo.update_task_description(task_id, description)
    if task:
        show_message(f"Task {task_id} updated successfully.", style="green")
    else:
        show_error(f"Task with ID {task_id} not found.")
        raise typer.Exit(code=1)

@cli.command(name="rm")
def rm(task_id: int):
    """Delete a task."""
    success = repo.delete_task(task_id)
    if success:
        show_message(f"Task {task_id} deleted successfully.", style="green")
    else:
        show_error(f"Task with ID {task_id} not found.")
        raise typer.Exit(code=1)

@cli.command(name="help")
def help_cmd():
    """Show help information."""
    from .ui import show_help
    show_help()
