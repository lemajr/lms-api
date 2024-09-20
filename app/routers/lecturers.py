from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import LecturerResponse, LecturerUpdate, LecturerCreate
from app.crud.lecturer import create_lecturer, get_lecturer, get_lecturers, update_lecturer, delete_lecturer
from app.utils.dependency import get_db

router = APIRouter()

# Create Lecturer
@router.post("/lecturer/", response_model=LecturerResponse)
def create_lecturer_route(lecturer: LecturerCreate, db: Session = Depends(get_db)):
    return create_lecturer(db, lecturer)

# Read Lecturer by ID
@router.get("/lecturer/{lecturer_id}", response_model=LecturerResponse)
def read_lecturer(lecturer_id: str, db: Session = Depends(get_db)):
    return get_lecturer(db, lecturer_id)

# Read All Lecturers
@router.get("/lecturers/", response_model=list[LecturerResponse])
def read_lecturers(db: Session = Depends(get_db)):
    return get_lecturers(db)

# Update Lecturer
@router.put("/lecturer/{lecturer_id}", response_model=LecturerResponse)
def update_lecturer_route(lecturer_id: str, lecturer: LecturerUpdate, db: Session = Depends(get_db)):
    return update_lecturer(db, lecturer_id, lecturer)

# Delete Lecturer (Soft Delete)
@router.delete("/lecturer/{lecturer_id}")
def delete_lecturer_route(lecturer_id: str, db: Session = Depends(get_db)):
    return delete_lecturer(db, lecturer_id)
