import pytest
import sys
from pathlib import Path
from typer.testing import CliRunner

# Add the src directory to path to ensure imports work correctly
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from todo_cli.commands import cli
from todo_cli.repository import TodoRepository
from todo_cli.models import TaskStatus

runner = CliRunner()

def test_add_and_ls():
    repo = TodoRepository()
    repo._tasks = {}
    repo._next_id = 1

    # Test Add
    result = runner.invoke(cli, ["add", "Buy milk"])
    assert result.exit_code == 0
    assert "Task added successfully!" in result.output
    assert "(ID: 1)" in result.output

    # Test List
    result = runner.invoke(cli, ["ls"])
    assert result.exit_code == 0
    assert "Buy milk" in result.output
    assert "PENDING" in result.output

def test_done_command():
    repo = TodoRepository()
    repo._tasks = {}
    repo._next_id = 1

    # Add a task first
    result = runner.invoke(cli, ["add", "Buy milk"])
    assert result.exit_code == 0
    assert "Task added successfully!" in result.output

    # Test Done
    result = runner.invoke(cli, ["done", "1"])
    assert result.exit_code == 0
    assert "Task 1 marked as completed." in result.output

    # Verify the task is now completed
    result = runner.invoke(cli, ["ls"])
    assert result.exit_code == 0
    assert "Buy milk" in result.output
    assert "COMPLETED" in result.output

def test_rm_command():
    repo = TodoRepository()
    repo._tasks = {}
    repo._next_id = 1

    # Add a task first
    result = runner.invoke(cli, ["add", "Buy milk"])
    assert result.exit_code == 0
    assert "Task added successfully!" in result.output

    # Test Remove
    result = runner.invoke(cli, ["rm", "1"])
    assert result.exit_code == 0
    assert "Task 1 deleted successfully." in result.output

    # Verify the task is gone
    result = runner.invoke(cli, ["ls"])
    assert result.exit_code == 0
    assert "Buy milk" not in result.output

def test_done_nonexistent_task():
    repo = TodoRepository()
    repo._tasks = {}
    repo._next_id = 1

    # Try to mark a non-existent task as done
    result = runner.invoke(cli, ["done", "999"])
    assert result.exit_code == 1
    assert "Error: Task with ID 999 not found." in result.output

def test_rm_nonexistent_task():
    repo = TodoRepository()
    repo._tasks = {}
    repo._next_id = 1

    # Try to remove a non-existent task
    result = runner.invoke(cli, ["rm", "999"])
    assert result.exit_code == 1
    assert "Error: Task with ID 999 not found." in result.output

def test_edit_command():
    repo = TodoRepository()
    repo._tasks = {}
    repo._next_id = 1

    # Add a task first
    result = runner.invoke(cli, ["add", "Buy milk"])
    assert result.exit_code == 0
    assert "Task added successfully!" in result.output

    # Test Edit
    result = runner.invoke(cli, ["edit", "1", "Buy almond milk"])
    assert result.exit_code == 0
    assert "Task 1 updated successfully." in result.output

    # Verify the task description is updated
    result = runner.invoke(cli, ["ls"])
    assert result.exit_code == 0
    assert "Buy almond milk" in result.output
    assert "Buy milk" not in result.output

def test_edit_nonexistent_task():
    repo = TodoRepository()
    repo._tasks = {}
    repo._next_id = 1

    # Try to edit a non-existent task
    result = runner.invoke(cli, ["edit", "999", "Updated description"])
    assert result.exit_code == 1
    assert "Error: Task with ID 999 not found." in result.output
