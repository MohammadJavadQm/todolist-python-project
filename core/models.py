"""
Defines the core data models for the application, including Project and Task.
"""
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

class Project:
    """Represents a project that contains a collection of tasks."""
    def __init__(self, name: str, description: str, project_id: int | None = None):
        self.id = project_id
        self.name = name
        self.description = description
        self.tasks: dict[int, Task] = {}  # A dictionary to hold tasks, keyed by task_id
        self._last_task_id = 0

    def add_task(self, title: str, description: str, deadline: date | None = None) -> Task:
        """
        Creates a new Task and adds it to the project.
        
        Args:
            title: The title of the task.
            description: The description of the task.
            deadline: The optional deadline for the task.

        Returns:
            The newly created Task object.
        """
        self._last_task_id += 1
        task = Task(title=title, description=description, task_id=self._last_task_id, deadline=deadline)
        self.tasks[task.id] = task
        return task

    def __repr__(self) -> str:
        """Provides a developer-friendly string representation of the project."""
        return f"<Project(id={self.id}, name='{self.name}')>"
