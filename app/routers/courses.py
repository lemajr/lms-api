from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.course import CourseCreate, CourseUpdate
from app.crud.course import create_course, get_course, get_courses, update_course, delete_course
from app.utils.dependency import get_db

router = APIRouter()

# Create Course
@router.post("/course/", response_model=CourseCreate)
def create_course_route(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db, course)

# Read Course by ID
@router.get("/course/{course_code}")
def read_course(course_code: str, db: Session = Depends(get_db)):
    return get_course(db, course_code)

# Read All Courses
@router.get("/courses/")
def read_courses(db: Session = Depends(get_db)):
    return get_courses(db)

# Update Course
@router.put("/course/{course_code}", response_model=CourseUpdate)
def update_course_route(course_code: str, course: CourseUpdate, db: Session = Depends(get_db)):
    return update_course(db, course_code, course)

# Delete Course (Soft Delete)
@router.delete("/course/{course_code}")
def delete_course_route(course_code: str, db: Session = Depends(get_db)):
    return delete_course(db, course_code)
