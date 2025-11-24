from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    due_date: Optional[datetime] = None
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True