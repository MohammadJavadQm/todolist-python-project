# File: core/models/task.py

from datetime import date
from enum import Enum

class TaskStatus(Enum):
    """Enumeration for the status of a task."""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task:
    """Represents a single task within a project."""
    def __init__(self, title: str, description: str, 
                 task_id: int, status: TaskStatus = TaskStatus.TODO, deadline: date | None = None):
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline

    def __repr__(self) -> str:
        """Provides a developer-friendly string representation of the task."""
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status.value}')>"