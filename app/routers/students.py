from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import StudentCreate, StudentUpdate, StudentResponse
from app.schemas.course import CourseResponse
from app.crud.student import create_student, get_student, get_students, update_student, delete_student, get_current_user
from app.utils import oauth2
from app.utils.dependency import get_db
from app.models.user import Student

router = APIRouter()

# Get current student's details
@router.get("/student/me", response_model=StudentResponse)
def get_current_student_me(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_user)
):
    # Constructing and returning the student response
    return StudentResponse(
        id=current_student.id,  
        full_name=current_student.full_name,
        email=current_student.email,
        student_reg_no=current_student.student_reg_no,
        created_at=current_student.created_at,
        updated_at=current_student.updated_at,
        is_deleted=current_student.is_deleted,
        is_active=current_student.is_active,
        courses=current_student.courses  # Assuming courses is a relationship
    )
    
# Get current student's courses
# @router.get("/student/me/courses", response_model=list[CourseResponse])
# def get_current_student_courses(
#     db: Session = Depends(get_db),
#     current_student: StudentResponse = Depends(oauth2.get_current_user)
# ):
#     return get_student_courses(db, current_student.reg_no)

# Create Student
@router.post("/student/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student_route(student: StudentCreate, db: Session = Depends(get_db), get_current_user: StudentResponse = Depends(oauth2.get_current_user)):
    return create_student(db, student)

# Read Student by ID
@router.get("/student/{reg_no}", response_model=StudentResponse)
def read_student(reg_no: str, db: Session = Depends(get_db), get_current_user: StudentResponse = Depends(oauth2.get_current_user)):
    return get_student(db, reg_no)

# Read All Students
@router.get("/students/", response_model=list[StudentResponse])
def read_students(db: Session = Depends(get_db), get_current_user: StudentResponse = Depends(oauth2.get_current_user)):
    return get_students(db)

# Update Student
@router.put("/student/{reg_no}", response_model=StudentResponse)
def update_student_route(reg_no: str, student: StudentUpdate, db: Session = Depends(get_db), get_current_user: StudentResponse = Depends(oauth2.get_current_user)):
    return update_student(db, reg_no, student)

# Delete Student (Soft Delete)
@router.delete("/student/{reg_no}", status_code=status.HTTP_200_OK)
def delete_student_route(reg_no: str, db: Session = Depends(get_db), get_current_user: StudentResponse = Depends(oauth2.get_current_user)):
    return delete_student(db, reg_no)
