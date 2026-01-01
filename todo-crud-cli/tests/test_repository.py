import pytest
import sys
from pathlib import Path

# Add the src directory to path to ensure imports work correctly
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from todo_cli.repository import TodoRepository
from todo_cli.models import TaskStatus

def test_add_task():
    repo = TodoRepository()
    # Reset repo for test (since it's a singleton)
    repo._tasks = {}
    repo._next_id = 1

    task = repo.add_task("Test task")
    assert task.id == 1
    assert task.description == "Test task"
    assert task.status == TaskStatus.PENDING
    assert len(repo.get_all_tasks()) == 1

def test_update_status():
    repo = TodoRepository()
    repo._tasks = {}
    repo._next_id = 1
    task = repo.add_task("Test")
    repo.update_task_status(task.id, TaskStatus.COMPLETED)
    assert repo.get_task(task.id).status == TaskStatus.COMPLETED

def test_update_description():
    repo = TodoRepository()
    repo._tasks = {}
    repo._next_id = 1
    task = repo.add_task("Test")
    updated_task = repo.update_task_description(task.id, "Updated test")
    assert updated_task.description == "Updated test"
    assert repo.get_task(task.id).description == "Updated test"

def test_delete_task():
    repo = TodoRepository()
    repo._tasks = {}
    repo._next_id = 1
    task = repo.add_task("Test")
    assert repo.delete_task(task.id) is True
    assert len(repo.get_all_tasks()) == 0
