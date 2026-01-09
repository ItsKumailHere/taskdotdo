import json
import os
from pathlib import Path
from typing import Dict, Any, List

class StorageManager:
    def __init__(self, storage_path: str = None):
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            self.storage_path = Path.home() / ".todo-app" / "tasks.json"

        # Ensure directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def load_tasks(self) -> Dict[str, Any]:
        """Loads tasks and next_id from JSON file."""
        if not self.storage_path.exists():
            return {"tasks": {}, "next_id": 1}

        try:
            with open(self.storage_path, "r") as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, IOError):
            return {"tasks": {}, "next_id": 1}

    def save_tasks(self, tasks: Dict[int, Any], next_id: int):
        """Saves tasks and next_id to JSON file atomically."""
        temp_path = self.storage_path.with_suffix(".tmp")

        # Convert Task objects or dicts to serializable format
        # and ensure keys are strings for JSON (ID is int)
        serializable_tasks = {
            str(k): (v.model_dump() if hasattr(v, "model_dump") else v)
            for k, v in tasks.items()
        }

        data = {
            "tasks": serializable_tasks,
            "next_id": next_id
        }

        try:
            with open(temp_path, "w") as f:
                json.dump(data, f, indent=4)
            os.replace(temp_path, self.storage_path)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise
