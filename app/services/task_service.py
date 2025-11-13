"""
Contains all business logic related to Task management.
"""
from datetime import date
from app.models.task import Task, TaskStatus
from storage.in_memory import InMemoryStorage

class TaskService:
    """Service layer for task-related operations."""
    def __init__(self, storage: InMemoryStorage, max_tasks_per_project: int):
        self._storage = storage
        self._max_tasks_per_project = max_tasks_per_project

    def add_task_to_project(self, project_id: int, title: str, description: str, deadline_str: str | None = None) -> Task:
        """Adds a new task to a project, enforcing business rules."""
        project = self._storage.get_project_by_id(project_id)
        if not project: 
            raise ValueError(f"Project with ID {project_id} not found.")
        if len(project.tasks) >= self._max_tasks_per_project: 
            raise Exception(f"Cannot add more tasks. Project '{project.name}' has reached the limit.")
        
        # CORRECTED: Enforce mandatory title
        if not title or not title.strip():
            raise ValueError("Task title is mandatory and cannot be empty.")
        if len(title.split()) > 30: 
            raise ValueError("Task title cannot exceed 30 words.")
        
        # CORRECTED: Only validate description if it's provided
        if description and len(description.split()) > 150: 
            raise ValueError("Task description cannot exceed 150 words.")
        
        deadline = None
        if deadline_str:
            try: 
                deadline = date.fromisoformat(deadline_str)
            except ValueError: 
                raise ValueError("Invalid deadline format. Use YYYY-MM-DD.")
        
        return project.add_task(title=title.strip(), description=description.strip(), deadline=deadline)

    def get_tasks_for_project(self, project_id: int) -> list[Task]:
        """Retrieves all tasks for a specific project."""
        project = self._storage.get_project_by_id(project_id)
        if not project: 
            raise ValueError(f"Project with ID {project_id} not found.")
        return list(project.tasks.values())

    def change_task_status(self, project_id: int, task_id: int, new_status_str: str) -> Task:
        """Changes the status of a specific task."""
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
        """Edits the details of a specific task."""
        task = self._storage.get_task_by_id(project_id, task_id)
        if not task: 
            raise ValueError(f"Task with ID {task_id} not found in project {project_id}.")
        
        if new_title is not None:
            # CORRECTED: Enforce mandatory title on edit
            if not new_title or not new_title.strip():
                raise ValueError("New task title is mandatory and cannot be empty.")
            if len(new_title.split()) > 30: 
                raise ValueError("New task title cannot exceed 30 words.")
            task.title = new_title.strip()

        if new_description is not None:
            # CORRECTED: Only validate description if it's provided
            if len(new_description.split()) > 150: 
                raise ValueError("New task description cannot exceed 150 words.")
            task.description = new_description.strip()

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
        """Deletes a task from a project."""
        if not self._storage.delete_task_by_id(project_id, task_id):
            raise ValueError(f"Task with ID {task_id} not found in project {project_id}.")
