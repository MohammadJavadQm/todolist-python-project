# File: core/models/project.py

from datetime import date
from .task import Task  # Import Task from the task.py file

class Project:
    """Represents a project that contains a collection of tasks."""
    def __init__(self, name: str, description: str, project_id: int | None = None):
        self.id = project_id
        self.name = name
        self.description = description
        self.tasks: dict[int, Task] = {}
        self._last_task_id = 0

    def add_task(self, title: str, description: str, deadline: date | None = None) -> Task:
        """Creates a new Task and adds it to the project."""
        self._last_task_id += 1
        task = Task(title=title, description=description, task_id=self._last_task_id, deadline=deadline)
        self.tasks[task.id] = task
        return task

    def __repr__(self) -> str:
        """Provides a developer-friendly string representation of the project."""
        return f"<Project(id={self.id}, name='{self.name}')>"