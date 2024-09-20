from pydantic import BaseModel
from typing import Optional
import uuid

# Base schema for Course
class CourseBase(BaseModel):
    course_code: str
    course_name: str

# Schema for Course creation
class CourseCreate(CourseBase):
    lecturer_id: uuid.UUID

# Response schema for Course
class CourseResponse(CourseBase):
    id: uuid.UUID
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True

# Schema for Course update
class CourseUpdate(CourseBase):
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    lecturer_id: Optional[uuid.UUID] = None  # Optional if you want to allow changing the lecturer

    class Config:
        from_attributes = True
