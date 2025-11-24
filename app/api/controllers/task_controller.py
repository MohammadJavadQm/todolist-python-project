from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import task_service
from app.api.controller_schemas.requests.task_request_schema import TaskCreateRequest, TaskUpdateRequest
from app.api.controller_schemas.responses.task_response_schema import TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(request: TaskCreateRequest, db: Session = Depends(get_db)):
    """
    Create a new task for a project.
    """
    # چک کردن وجود پروژه باید در سرویس انجام شود، اما هندل کردن خطا اینجا رخ می‌دهد
    try:
        return task_service.create_task(db, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[TaskResponse])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all tasks.
    """
    return task_service.get_tasks(db, skip, limit)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get a specific task by ID.
    """
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, request: TaskUpdateRequest, db: Session = Depends(get_db)):
    """
    Update a task (e.g., mark as done).
    """
    task = task_service.update_task(db, task_id, request)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task.
    """
    success = task_service.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None