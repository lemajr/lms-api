from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import Lecturer
from app.schemas.user import LecturerCreate, LecturerUpdate
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError

# Create Lecturer
def create_lecturer(db: Session, lecturer: LecturerCreate):
    existing_lecturer = db.query(Lecturer).filter(
        (Lecturer.email == lecturer.email) | (Lecturer.lecturer_id == lecturer.lecturer_id),
        Lecturer.is_deleted == False
    ).first()

    if existing_lecturer:
        raise HTTPException(status_code=400, detail="Lecturer with this email or lecturer ID already exists.")

    try:
        db_lecturer = Lecturer(
            full_name=lecturer.full_name,
            email=lecturer.email,
            lecturer_id=lecturer.lecturer_id,
            password_hash=hash_password(lecturer.password),
        )
        db.add(db_lecturer)
        db.commit()
        db.refresh(db_lecturer)
        return db_lecturer
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Lecturer creation failed due to integrity issues.")

# Read Lecturer by ID
def get_lecturer(db: Session, lecturer_id: str):
    lecturer = db.query(Lecturer).filter(Lecturer.lecturer_id == lecturer_id, Lecturer.is_deleted == False).first()
    if not lecturer:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    return lecturer

# Read All Lecturers
def get_lecturers(db: Session):
    return db.query(Lecturer).filter(Lecturer.is_deleted == False).all()

# Update Lecturer
def update_lecturer(db: Session, lecturer_id: str, lecturer_update: LecturerUpdate):
    db_lecturer = get_lecturer(db, lecturer_id)
    if lecturer_update.full_name:
        db_lecturer.full_name = lecturer_update.full_name
    if lecturer_update.email:
        db_lecturer.email = lecturer_update.email
    if lecturer_update.password:
        db_lecturer.password_hash = hash_password(lecturer_update.password)
    
    db.commit()
    db.refresh(db_lecturer)
    return db_lecturer

# Soft Delete Lecturer
def delete_lecturer(db: Session, lecturer_id: str):
    db_lecturer = get_lecturer(db, lecturer_id)
    db_lecturer.is_deleted = True
    db.commit()
    return {"message": "Lecturer successfully deleted"}
