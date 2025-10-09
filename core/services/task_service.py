# File: core/services/task_service.py

from datetime import date
from core.models import Task, TaskStatus
from storage.in_memory import InMemoryStorage

class TaskService:
    """Service layer that orchestrates operations on tasks."""
    def __init__(self, storage: InMemoryStorage, max_tasks_per_project: int):
        self._storage = storage
        self._max_tasks_per_project = max_tasks_per_project

    def add_task_to_project(self, project_id: int, title: str, description: str, deadline_str: str | None = None) -> Task:
        project = self._storage.get_project_by_id(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found.")
        if len(project.tasks) >= self._max_tasks_per_project:
            raise Exception(f"Cannot add more tasks. Project '{project.name}' has reached the limit.")
        if len(title.split()) > 30:
            raise ValueError("Task title cannot exceed 30 words.")
        if len(description.split()) > 150:
            raise ValueError("Task description cannot exceed 150 words.")
        
        deadline = None
        if deadline_str:
            try:
                deadline = date.fromisoformat(deadline_str)
            except ValueError:
                raise ValueError("Invalid deadline format. Please use YYYY-MM-DD.")
        
        return self._storage.create_task(project_id, title, description, deadline)

    def get_tasks_for_project(self, project_id: int) -> list[Task]:
        project = self._storage.get_project_by_id(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found.")
        return list(project.tasks.values())

    def change_task_status(self, project_id: int, task_id: int, new_status_str: str) -> Task:
        try:
            new_status = TaskStatus(new_status_str.lower())
        except ValueError:
            raise ValueError(f"'{new_status_str}' is not a valid status. Use 'todo', 'doing', or 'done'.")
        
        task = self._storage.get_task_by_id(project_id, task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found in project {project_id}.")
        task.status = new_status
        return task

    def edit_task(self, project_id: int, task_id: int, new_title: str | None = None, new_description: str | None = None, new_deadline_str: str | None = None) -> Task:
        task = self._storage.get_task_by_id(project_id, task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found in project {project_id}.")
        if new_title is not None:
            if len(new_title.split()) > 30:
                raise ValueError("New task title cannot exceed 30 words.")
            task.title = new_title
        if new_description is not None:
            if len(new_description.split()) > 150:
                raise ValueError("New task description cannot exceed 150 words.")
            task.description = new_description
        if new_deadline_str is not None:
            if new_deadline_str.lower() == 'none':
                task.deadline = None
            else:
                try:
                    task.deadline = date.fromisoformat(new_deadline_str)
                except ValueError:
                    raise ValueError("Invalid deadline format. Use YYYY-MM-DD.")
        return task

    def delete_task(self, project_id: int, task_id: int):
        if not self._storage.delete_task_by_id(project_id, task_id):
            raise ValueError(f"Task with ID {task_id} not found in project {project_id}.")