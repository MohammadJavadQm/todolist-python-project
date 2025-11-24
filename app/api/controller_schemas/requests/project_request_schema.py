from pydantic import BaseModel, Field
from typing import Optional

class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Name of the project")
    description: Optional[str] = Field(None, max_length=200, description="Description of the project")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "University Projects",
                "description": "All tasks related to university courses"
            }
        }

class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=200)