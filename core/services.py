"""
Contains the core business logic and services for managing projects and tasks.
"""
from datetime import date
from core.models import Project, Task, TaskStatus
from storage.in_memory import InMemoryStorage

class ProjectService:
    """
    Service layer that orchestrates operations on projects and tasks,
    enforcing all business rules.
    """
    def __init__(self, storage: InMemoryStorage, max_projects: int, max_tasks_per_project: int):
        self._storage = storage
        self._max_projects = max_projects
        self._max_tasks_per_project = max_tasks_per_project

    # --- Project Management Methods ---

    def create_project(self, name: str, description: str) -> Project:
        """Creates a new project after validating all business rules."""
        # The rule is <= 30 words, so we raise an error if it's > 30.
        if len(name.split()) > 30: 
            raise ValueError("Project name cannot exceed 30 words.")
        
        # The rule is <= 150 words, so we raise an error if it's > 150.
        if len(description.split()) > 150: 
            raise ValueError("Project description cannot exceed 150 words.")
        
        if self._storage.get_project_by_name(name): 
            raise ValueError(f"A project with the name '{name}' already exists.")
        
        if len(self._storage.get_all_projects()) >= self._max_projects: 
            raise Exception("Cannot create more projects. The maximum limit has been reached.")
            
        return self._storage.create(name, description)

    def edit_project(self, project_id: int, new_name: str | None = None, new_description: str | None = None) -> Project:
        """Edits an existing project's details."""
        project = self._storage.get_project_by_id(project_id)
        if not project: 
            raise ValueError(f"Project with ID {project_id} not found.")
        
        if new_name is not None:
            if len(new_name.split()) > 30: 
                raise ValueError("New project name cannot exceed 30 words.")
            existing_project = self._storage.get_project_by_name(new_name)
            if existing_project and existing_project.id != project_id: 
                raise ValueError(f"Another project with the name '{new_name}' already exists.")
            project.name = new_name

        if new_description is not None:
            if len(new_description.split()) > 150: 
                raise ValueError("New project description cannot exceed 150 words.")
            project.description = new_description
            
        return project

    def delete_project(self, project_id: int):
        """Deletes a project and all its tasks (cascade delete)."""
        if not self._storage.delete_project_by_id(project_id):
            raise ValueError(f"Project with ID {project_id} not found.")

    def get_all_projects(self) -> list[Project]:
        """Returns a list of all projects."""
        return self._storage.get_all_projects()

    # --- Task Management Methods ---

    def add_task_to_project(self, project_id: int, title: str, description: str, deadline_str: str | None = None) -> Task:
        """Adds a new task to a specific project."""
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
                raise ValueError("Invalid deadline format. Please use YY YY-MM-DD.")
        
        return project.add_task(title=title, description=description, deadline=deadline)

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
        """Deletes a task from a project."""
        if not self._storage.delete_task_by_id(project_id, task_id):
            raise ValueError(f"Task with ID {task_id} not found in project {project_id}.")