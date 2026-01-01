# Repository for in-memory storage of tasks
from typing import List, Optional
from .models import Task, TaskStatus

class TodoRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TodoRepository, cls).__new__(cls)
            cls._instance._tasks = {}
            cls._instance._next_id = 1
        return cls._instance

    def add_task(self, description: str) -> Task:
        task = Task(id=self._next_id, description=description, status=TaskStatus.PENDING)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_all_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        # Newest first logic (descending by ID)
        return sorted(tasks, key=lambda x: x.id, reverse=True)

    def get_task(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def update_task_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        if task_id in self._tasks:
            self._tasks[task_id].status = status
            return self._tasks[task_id]
        return None

    def update_task_description(self, task_id: int, description: str) -> Optional[Task]:
        if task_id in self._tasks:
            self._tasks[task_id].description = description
            return self._tasks[task_id]
        return None

    def delete_task(self, task_id: int) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
