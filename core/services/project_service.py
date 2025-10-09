# File: core/services/project_service.py

from core.models import Project
from storage.in_memory import InMemoryStorage

class ProjectService:
    """Service layer that orchestrates operations on projects."""
    def __init__(self, storage: InMemoryStorage, max_projects: int):
        self._storage = storage
        self._max_projects = max_projects

    def create_project(self, name: str, description: str) -> Project:
        if len(name.split()) > 30:
            raise ValueError("Project name cannot exceed 30 words.")
        if len(description.split()) > 150:
            raise ValueError("Project description cannot exceed 150 words.")
        if self._storage.get_project_by_name(name):
            raise ValueError(f"A project with the name '{name}' already exists.")
        if len(self._storage.get_all_projects()) >= self._max_projects:
            raise Exception("Cannot create more projects. The maximum limit has been reached.")
        return self._storage.create_project(name, description)

    def edit_project(self, project_id: int, new_name: str | None = None, new_description: str | None = None) -> Project:
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
        if not self._storage.delete_project_by_id(project_id):
            raise ValueError(f"Project with ID {project_id} not found.")

    def get_all_projects(self) -> list[Project]:
        return self._storage.get_all_projects()