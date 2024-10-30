from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import LecturerResponse, LecturerUpdate, LecturerCreate
from app.crud.lecturer import create_lecturer, get_lecturer, get_lecturers, update_lecturer, delete_lecturer, get_current_lecturer
from app.utils import oauth2
from app.utils.dependency import get_db
from app.models.user import Lecturer

router = APIRouter()


# Get current Lecturer's details
@router.get("/lecturer/me", response_model=LecturerResponse)
def get_current_Lecturer_me(
    db: Session = Depends(get_db),
    current_Lecturer: Lecturer = Depends(get_current_lecturer)
):
    # Constructing and returning the Lecturer response
    return LecturerResponse(
        id=current_Lecturer.id,  
        full_name=current_Lecturer.full_name,
        email=current_Lecturer.email,
        lecturer_id=current_Lecturer.lecturer_id,
        created_at=current_Lecturer.created_at,
        updated_at=current_Lecturer.updated_at,
        is_deleted=current_Lecturer.is_deleted,
        is_active=current_Lecturer.is_active,
        courses=current_Lecturer.courses  # courses is a relationship
    )

# Create Lecturer
@router.post("/lecturer/", response_model=LecturerResponse)
def create_lecturer_route(lecturer: LecturerCreate, db: Session = Depends(get_db), get_current_user: LecturerResponse = Depends(oauth2.get_current_user)):
    return create_lecturer(db, lecturer)

# Read Lecturer by ID
@router.get("/lecturer/{lecturer_id}", response_model=LecturerResponse)
def read_lecturer(lecturer_id: str, db: Session = Depends(get_db), get_current_user: LecturerResponse = Depends(oauth2.get_current_user)):
    return get_lecturer(db, lecturer_id)

# Read All Lecturers
@router.get("/lecturers/", response_model=list[LecturerResponse])
def read_lecturers(db: Session = Depends(get_db), get_current_user: LecturerResponse = Depends(oauth2.get_current_user)):
    return get_lecturers(db)

# Update Lecturer
@router.put("/lecturer/{lecturer_id}", response_model=LecturerResponse)
def update_lecturer_route(lecturer_id: str, lecturer: LecturerUpdate, db: Session = Depends(get_db), get_current_user: LecturerResponse = Depends(oauth2.get_current_user)):
    return update_lecturer(db, lecturer_id, lecturer)

# Delete Lecturer (Soft Delete)
@router.delete("/lecturer/{lecturer_id}")
def delete_lecturer_route(lecturer_id: str, db: Session = Depends(get_db), get_current_user: LecturerResponse = Depends(oauth2.get_current_user)):
    return delete_lecturer(db, lecturer_id)
