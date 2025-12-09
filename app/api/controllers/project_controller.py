from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import project_service
from app.api.controller_schemas.requests.project_request_schema import ProjectCreateRequest, ProjectUpdateRequest
from app.api.controller_schemas.responses.project_response_schema import ProjectResponse

router = APIRouter()

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(request: ProjectCreateRequest, db: Session = Depends(get_db)):
    """
    Create a new project.
    This endpoint creates a new resource in the database.
    """
    return project_service.create_project(db, request)

@router.get("/", response_model=List[ProjectResponse])
def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all projects with pagination.
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    return project_service.get_projects(db, skip, limit)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """
    Get a specific project by ID.
    """
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, request: ProjectUpdateRequest, db: Session = Depends(get_db)):
    """
    Update a project.
    """
    project = project_service.update_project(db, project_id, request)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """
    Delete a project.
    """
    success = project_service.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    # در وضعیت 204 معمولاً چیزی برنمی‌گردانیم (یا فقط Response خالی)
    return None