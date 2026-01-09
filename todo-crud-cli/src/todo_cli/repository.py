from typing import List, Optional, Dict
from threading import Lock
from .models import Task, TaskStatus
from .storage import StorageManager

class TodoRepository:
    _instance: Optional['TodoRepository'] = None
    _lock: Lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(TodoRepository, cls).__new__(cls)
                cls._instance._storage = StorageManager()
                data = cls._instance._storage.load_tasks()

                # Convert loaded dicts back to Task objects
                cls._instance._tasks = {
                    int(k): Task(**v) for k, v in data.get("tasks", {}).items()
                }
                cls._instance._next_id = data.get("next_id", 1)
            return cls._instance

    def _save(self):
        """Helper to trigger persistence."""
        self._storage.save_tasks(self._tasks, self._next_id)

    def add_task(self, description: str) -> Task:
        task = Task(id=self._next_id, description=description)
        self._tasks[self._next_id] = task
        self._next_id += 1
        self._save()
        return task

    def get_all_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return sorted(tasks, key=lambda x: x.id, reverse=True)

    def get_task(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def update_task_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        if task_id in self._tasks:
            self._tasks[task_id].status = status
            self._save()
            return self._tasks[task_id]
        return None

    def update_task_description(self, task_id: int, description: str) -> Optional[Task]:
        if task_id in self._tasks:
            self._tasks[task_id].description = description
            self._save()
            return self._tasks[task_id]
        return None

    def delete_task(self, task_id: int) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._save()
            return True
        return False

    def delete_all_tasks(self) -> int:
        """Delete all tasks. Returns count of deleted tasks."""
        count = len(self._tasks)
        self._tasks.clear()
        self._save()
        return count

    def delete_completed_tasks(self) -> int:
        """Delete all completed tasks. Returns count of deleted tasks."""
        completed_ids = [
            task_id for task_id, task in self._tasks.items()
            if task.status == TaskStatus.COMPLETED
        ]
        for task_id in completed_ids:
            del self._tasks[task_id]
        self._save()
        return len(completed_ids)
