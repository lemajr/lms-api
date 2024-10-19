from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union
from uuid import UUID
from datetime import datetime

# Response schema for Course related to Students
class CourseResponse(BaseModel):
    id: UUID
    course_code: str
    course_name: str
    lecturer_id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

# Student Base Schema
class StudentBase(BaseModel):
    full_name: str
    email: EmailStr
    student_reg_no: str

# Schema for Student creation
class StudentCreate(StudentBase):
    password: str

# Response schema for Student
class StudentResponse(StudentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    is_active: bool
    courses: Optional[List[CourseResponse]] = None  # List of courses enrolled

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
    
    

# Schema for Student update
class StudentUpdate(StudentBase):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    student_reg_no: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True

# Lecturer Base Schema
class LecturerBase(BaseModel):
    full_name: str
    email: EmailStr
    lecturer_id: str

# Schema for Lecturer creation
class LecturerCreate(LecturerBase):
    password: str

# Response schema for Lecturer
class LecturerResponse(LecturerBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    is_active: bool

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

# Schema for Lecturer update
class LecturerUpdate(LecturerBase):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    lecturer_id: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True
        

# Admin Base Schema
class AdminBase(BaseModel):
    full_name: str
    email: EmailStr
    admin_id: str

# Schema for Admin creation
class AdminCreate(AdminBase):
    password: str

# Response schema for Admin
class AdminResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    admin_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_deleted: bool

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

        
# Schema for Admin update
class AdminUpdate(AdminBase):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    admin_id: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True

# Authentication Schema

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    student_reg_no: Optional[str] = None
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    is_active: Optional[bool] = None
    courses: Optional[List[CourseResponse]] = None  # List of courses enrolled

# Combined User Response schema that handles Student, Lecturer, and Admin
class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_deleted: bool
    # Dynamically include either a StudentResponse, LecturerResponse, or AdminResponse
    user_data: Optional[Union[StudentResponse, LecturerResponse, AdminResponse]] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }