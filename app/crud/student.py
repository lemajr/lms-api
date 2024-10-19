from uuid import UUID
from fastapi import HTTPException, Depends,status
from sqlalchemy.orm import Session
from app.models.user import Student
from app.schemas.user import StudentCreate, StudentUpdate,TokenData
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError
from app.utils.dependency import get_db
from app.utils.oauth2 import oauth2_scheme  
from app.utils.token import verify_token 

# Get the current user from the database    
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme) 
) -> Student:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Verify the token and extract user data
    token_data = verify_token(token, credentials_exception)
    
    # Fetch the student using `student_reg_no` from token data
    student = (
        db.query(Student)
        .filter(Student.student_reg_no == token_data.username, Student.is_deleted == False)
        .first()
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student



# Create Student
def create_student(db: Session, student: StudentCreate):
    existing_student = db.query(Student).filter(
        (Student.email == student.email) | (Student.student_reg_no == student.student_reg_no),
        Student.is_deleted == False
    ).first()

    if existing_student:
        raise HTTPException(status_code=400, detail="Student with this email or regiUUIDation number already exists.")

    try:
        db_student = Student(
            full_name=student.full_name,
            email=student.email,
            student_reg_no=student.student_reg_no,
            password_hash=hash_password(student.password),
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Lecturer with this email or lecturer ID already exists..")

# Read Student by ID
def get_student(db: Session, student_reg_no: UUID):
    student = db.query(Student).filter(Student.id == student_reg_no, Student.is_deleted == False).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# Read All Students
def get_students(db: Session):
    db_all = db.query(Student).filter(Student.is_deleted == False).all()
    if not db_all:
        raise HTTPException(status_code=404, detail="No lecturers found")
    return db_all


# Update Student
def update_student(db: Session, student_reg_no: UUID, student_update: StudentUpdate):
    db_admin = get_student(db, student_reg_no)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    # Check for unique constraints
    if student_update.email:
        existing_lecturer = db.query(Student).filter(
            Student.email == student_update.email,
            Student.is_deleted == False
        ).first()
        if existing_lecturer and existing_lecturer.student_reg_no != student_reg_no:
            raise HTTPException(status_code=400, detail="Email already in use by another Student.")

    if student_update.student_reg_no:
        existing_lecturer = db.query(Student).filter(
            Student.student_reg_no == student_update.student_reg_no,
            Student.is_deleted == False
        ).first()
        if existing_lecturer and existing_lecturer.student_reg_no != student_reg_no:
            raise HTTPException(status_code=400, detail="Lecturer ID already in use by another Student.")

    db_student = get_student(db, student_reg_no)
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
def delete_student(db: Session, student_reg_no: UUID):
    db_student = get_student(db, student_reg_no)
    db_student.is_deleted = True
    db.commit()
    return {"message": "Student successfully deleted"}
