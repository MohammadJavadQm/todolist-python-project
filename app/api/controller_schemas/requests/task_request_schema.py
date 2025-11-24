from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    project_id: int = Field(..., gt=0, description="The ID of the project this task belongs to")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete Phase 3",
                "description": "Implement FastAPI schemas",
                "due_date": "2025-11-30T10:00:00",
                "project_id": 1
            }
        }

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(Pending|Doing|Done)$") # چک کردن وضعیت مجاز