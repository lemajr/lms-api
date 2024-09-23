from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import StudentCreate, StudentUpdate, StudentResponse
from app.crud.student import create_student, get_student, get_students, update_student, delete_student
from app.utils import oauth2
from app.utils.dependency import get_db

router = APIRouter()

# Create Student
@router.post("/student/", response_model=StudentResponse)
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
@router.delete("/student/{reg_no}")
def delete_student_route(reg_no: str, db: Session = Depends(get_db), get_current_user: StudentResponse = Depends(oauth2.get_current_user)):
    return delete_student(db, reg_no)
