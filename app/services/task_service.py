from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.api.controller_schemas.requests.task_request_schema import TaskCreateRequest, TaskUpdateRequest

MAX_TASKS_PER_PROJECT = 100

def create_task(db: Session, request: TaskCreateRequest) -> Task:
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)

    # 1. بررسی وجود پروژه
    project = project_repo.get_project_by_id(request.project_id)
    if not project:
        raise ValueError(f"Project with ID {request.project_id} not found.")

    # 2. بررسی سقف تعداد تسک
    if len(project.tasks) >= MAX_TASKS_PER_PROJECT:
        raise ValueError(f"Cannot add more tasks. Project '{project.name}' has reached the limit.")

    # 3. بررسی تعداد کلمات
    if len(request.title.split()) > 30:
        raise ValueError("Task title cannot exceed 30 words.")
    
    if request.description and len(request.description.split()) > 150:
        raise ValueError("Task description cannot exceed 150 words.")

    # 4. ایجاد تسک (تبدیل تاریخ توسط Pydantic انجام شده است)
    return task_repo.add_task_to_project(
        project=project,
        title=request.title,
        description=request.description,
        deadline=request.due_date 
    )

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    repo = TaskRepository(db)
    return db.query(Task).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    repo = TaskRepository(db)
    return repo.get_task_by_id(task_id)

def update_task(db: Session, task_id: int, request: TaskUpdateRequest):
    repo = TaskRepository(db)
    task = repo.get_task_by_id(task_id)
    if not task:
        return None

    if request.title:
        if len(request.title.split()) > 30:
            raise ValueError("New task title cannot exceed 30 words.")
        task.title = request.title

    if request.description:
        if len(request.description.split()) > 150:
            raise ValueError("New task description cannot exceed 150 words.")
        task.description = request.description
    
    if request.due_date is not None:
        task.deadline = request.due_date
        
    if request.status:
        # تبدیل رشته به Enum
        try:
            task.status = TaskStatus(request.status.lower())
        except ValueError:
            raise ValueError("Invalid status")

    return repo.update_task(task)

def delete_task(db: Session, task_id: int):
    repo = TaskRepository(db)
    task = repo.get_task_by_id(task_id)
    if not task:
        return False
    repo.delete_task(task)
    return True