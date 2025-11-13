"""
Contains all business logic related to Project management.
"""
from app.models.project import Project
from storage.in_memory import InMemoryStorage

class ProjectService:
    """Service layer for project-related operations."""
    def __init__(self, storage: InMemoryStorage, max_projects: int):
        self._storage = storage
        self._max_projects = max_projects

    def create_project(self, name: str, description: str) -> Project:
        """Creates a new project, enforcing business rules."""
        # CORRECTED: Enforce mandatory name
        if not name or not name.strip():
            raise ValueError("Project name is mandatory and cannot be empty.")

        if len(name.split()) > 30: 
            raise ValueError("Project name cannot exceed 30 words.")
        
        # CORRECTED: Only validate description if it's provided
        if description and len(description.split()) > 150: 
            raise ValueError("Project description cannot exceed 150 words.")
        
        if self._storage.get_project_by_name(name.strip()): 
            raise ValueError(f"A project with the name '{name.strip()}' already exists.")
        
        if len(self._storage.get_all_projects()) >= self._max_projects: 
            raise Exception("Cannot create more projects. The maximum limit has been reached.")
            
        return self._storage.create(name.strip(), description.strip())

    def edit_project(self, project_id: int, new_name: str | None = None, new_description: str | None = None) -> Project:
        """Edits an existing project's details."""
        project = self._storage.get_project_by_id(project_id)
        if not project: 
            raise ValueError(f"Project with ID {project_id} not found.")
        
        if new_name is not None:
            # CORRECTED: Enforce mandatory name on edit
            if not new_name or not new_name.strip():
                raise ValueError("New project name is mandatory and cannot be empty.")
            if len(new_name.split()) > 30: 
                raise ValueError("New project name cannot exceed 30 words.")
            existing_project = self._storage.get_project_by_name(new_name.strip())
            if existing_project and existing_project.id != project_id: 
                raise ValueError(f"Another project with the name '{new_name.strip()}' already exists.")
            project.name = new_name.strip()

        if new_description is not None:
            # CORRECTED: Only validate description if it's provided
            if len(new_description.split()) > 150: 
                raise ValueError("New project description cannot exceed 150 words.")
            project.description = new_description.strip()
            
        return project

    def delete_project(self, project_id: int):
        """Deletes a project."""
        if not self._storage.delete_project_by_id(project_id):
            raise ValueError(f"Project with ID {project_id} not found.")

    def get_all_projects(self) -> list[Project]:
        """Returns all projects."""
        return self._storage.get_all_projects()
