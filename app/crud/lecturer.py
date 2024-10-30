from uuid import UUID
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.user import Lecturer
from app.schemas.user import LecturerCreate, LecturerUpdate
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError
from app.utils.dependency import get_db
from app.utils.oauth2 import oauth2_scheme  
from app.utils.token import verify_token 

# Get the current user from the database    
def get_current_lecturer(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme) 
) -> Lecturer:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Verify the token and extract user data
    token_data = verify_token(token, credentials_exception)
    
    # Fetch the Lecturer using `Lecturer_reg_no` from token data
    lecturer = (
        db.query(Lecturer)
        .filter(Lecturer.lecturer_id == token_data.username, Lecturer.is_deleted == False)
        .first()
    )
    if not lecturer:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    return lecturer


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
        raise HTTPException(status_code=400, detail="Lecturer with this email or lecturer ID already exists.")

# Read Lecturer by ID
def get_lecturer(db: Session, lecturer_id: UUID):
    lecturer = db.query(Lecturer).filter(Lecturer.id == lecturer_id, Lecturer.is_deleted == False).first()
    if not lecturer:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    return lecturer


# Read All Lecturers
def get_lecturers(db: Session):
    db_all = db.query(Lecturer).filter(Lecturer.is_deleted == False).all()
    if not db_all:
        raise HTTPException(status_code=404, detail="No lecturers found")
    return db_all

# Update Lecturer
def update_lecturer(db: Session, lecturer_id: UUID, lecturer_update: LecturerUpdate):
    db_admin = get_lecturer(db, lecturer_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    # Check for unique constraints
    if lecturer_update.email:
        existing_lecturer = db.query(Lecturer).filter(
            Lecturer.email == lecturer_update.email,
            Lecturer.is_deleted == False
        ).first()
        if existing_lecturer and existing_lecturer.lecturer_id != lecturer_id:
            raise HTTPException(status_code=400, detail="Email already in use by another Lecturer.")

    if lecturer_update.lecturer_id:
        existing_lecturer = db.query(Lecturer).filter(
            Lecturer.lecturer_id == lecturer_update.lecturer_id,
            Lecturer.is_deleted == False
        ).first()
        if existing_lecturer and existing_lecturer.lecturer_id != lecturer_id:
            raise HTTPException(status_code=400, detail="Lecturer ID already in use by another Lecturer.")


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
