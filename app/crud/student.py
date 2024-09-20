from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import Student
from app.schemas.user import StudentCreate, StudentUpdate
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError

# Create Student
def create_student(db: Session, student: StudentCreate):
    existing_student = db.query(Student).filter(
        (Student.email == student.email) | (Student.reg_no == student.reg_no),
        Student.is_deleted == False
    ).first()

    if existing_student:
        raise HTTPException(status_code=400, detail="Student with this email or registration number already exists.")

    try:
        db_student = Student(
            full_name=student.full_name,
            email=student.email,
            reg_no=student.reg_no,
            password_hash=hash_password(student.password),
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Student creation failed due to integrity issues.")

# Read Student by ID
def get_student(db: Session, reg_no: str):
    student = db.query(Student).filter(Student.reg_no == reg_no, Student.is_deleted == False).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Read All Students
def get_students(db: Session):
    return db.query(Student).filter(Student.is_deleted == False).all()

# Update Student
def update_student(db: Session, reg_no: str, student_update: StudentUpdate):
    db_student = get_student(db, reg_no)
    if student_update.full_name:
        db_student.full_name = student_update.full_name
    if student_update.email:
        db_student.email = student_update.email
    if student_update.password:
        db_student.password_hash = hash_password(student_update.password)
    
    db.commit()
    db.refresh(db_student)
    return db_student

# Soft Delete Student
def delete_student(db: Session, reg_no: str):
    db_student = get_student(db, reg_no)
    db_student.is_deleted = True
    db.commit()
    return {"message": "Student successfully deleted"}
