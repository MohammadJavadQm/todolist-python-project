from sqlalchemy.orm import Session
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.api.controller_schemas.requests.project_request_schema import ProjectCreateRequest, ProjectUpdateRequest

# تنظیمات بیزینسی (می‌تواند از متغیر محیطی خوانده شود)
MAX_PROJECTS_LIMIT = 50

def create_project(db: Session, request: ProjectCreateRequest) -> Project:
    """یک پروژه جدید ایجاد می‌کند."""
    repo = ProjectRepository(db)

    # 1. بیزینس لاجیک: بررسی سقف تعداد پروژه‌ها
    if len(repo.get_all_projects()) >= MAX_PROJECTS_LIMIT:
        raise ValueError("Cannot create more projects. The maximum limit has been reached.")

    # 2. بیزینس لاجیک: نام تکراری
    if repo.get_project_by_name(request.name):
        raise ValueError(f"A project with the name '{request.name}' already exists.")

    # 3. بیزینس لاجیک: تعداد کلمات (علاوه بر تعداد کاراکتر که Pydantic چک کرده)
    if len(request.name.split()) > 30:
        raise ValueError("Project name cannot exceed 30 words.")
    
    if request.description and len(request.description.split()) > 150:
        raise ValueError("Project description cannot exceed 150 words.")

    # 4. ذخیره
    return repo.create_project(name=request.name, description=request.description)

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    repo = ProjectRepository(db)
    return repo.get_all_projects()[skip : skip + limit]

def get_project(db: Session, project_id: int):
    repo = ProjectRepository(db)
    return repo.get_project_by_id(project_id)

def update_project(db: Session, project_id: int, request: ProjectUpdateRequest):
    repo = ProjectRepository(db)
    project = repo.get_project_by_id(project_id)
    if not project:
        return None

    if request.name:
        # چک نام تکراری در آپدیت
        existing = repo.get_project_by_name(request.name)
        if existing and existing.id != project_id:
            raise ValueError(f"Another project with name '{request.name}' already exists.")
        
        if len(request.name.split()) > 30:
            raise ValueError("New project name cannot exceed 30 words.")
        project.name = request.name

    if request.description:
        if len(request.description.split()) > 150:
            raise ValueError("New project description cannot exceed 150 words.")
        project.description = request.description

    return repo.update_project(project)

def delete_project(db: Session, project_id: int):
    repo = ProjectRepository(db)
    project = repo.get_project_by_id(project_id)
    if not project:
        return False
    repo.delete_project(project)
    return True