# File: storage/in_memory.py

"""
Provides an in-memory storage solution for projects and tasks.
This storage is ephemeral and will be reset every time the application starts.
"""
from datetime import date
# The import remains correct because of our __init__.py in the models folder.
from core.models import Project, Task

class InMemoryStorage:
    """Manages all data in memory using Python dictionaries."""
    def __init__(self):
        self._projects: dict[int, Project] = {}
        self._last_project_id = 0

    # --- Project Methods ---

    # RENAMED: from `create` to `create_project` for clarity
    def create_project(self, name: str, description: str) -> Project:
        """Creates a new project and stores it in memory."""
        self._last_project_id += 1
        project = Project(name=name, description=description, project_id=self._last_project_id)
        self._projects[self._last_project_id] = project
        return project

    def get_project_by_name(self, name: str) -> Project | None:
        """Finds a project by its exact name."""
        for project in self._projects.values():
            if project.name == name:
                return project
        return None

    def get_all_projects(self) -> list[Project]:
        """Returns a list of all projects."""
        return list(self._projects.values())
    
    def get_project_by_id(self, project_id: int) -> Project | None:
        """Retrieves a single project by its unique ID."""
        return self._projects.get(project_id)

    def delete_project_by_id(self, project_id: int) -> bool:
        """Deletes a project by its ID. Returns True if successful, False otherwise."""
        if project_id in self._projects:
            del self._projects[project_id]
            return True
        return False

    # --- Task Methods ---

    # NEW: Added `create_task` method for the TaskService to use
    def create_task(self, project_id: int, title: str, description: str, deadline: date | None) -> Task | None:
        """Creates a new task and adds it to the specified project."""
        project = self.get_project_by_id(project_id)
        if not project:
            return None
        # We call the project's own method to handle the logic of adding the task
        new_task = project.add_task(title=title, description=description, deadline=deadline)
        return new_task
    
    def get_task_by_id(self, project_id: int, task_id: int) -> Task | None:
        """Finds a specific task within a specific project."""
        project = self.get_project_by_id(project_id)
        if project:
            return project.tasks.get(task_id)
        return None

    def delete_task_by_id(self, project_id: int, task_id: int) -> bool:
        """Deletes a task from a project. Returns True if successful."""
        project = self.get_project_by_id(project_id)
        if project and task_id in project.tasks:
            del project.tasks[task_id]
            return True
        return False