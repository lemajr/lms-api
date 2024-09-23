from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import Lecturer
from sqlalchemy.exc import IntegrityError
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate

# Create Course
def create_course(db: Session, course: CourseCreate):
    existing_course = db.query(Course).filter(
        (Course.course_code == course.course_code),
        Course.is_deleted == False
    ).first()

    if existing_course:
        raise HTTPException(status_code=400, detail="Course with this course code already exists.")

    try:
        db_course = Course(
            course_name=course.course_name,
            course_code=course.course_code,
            lecturer_id=course.lecturer_id
        )
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Course with this course code already exists.")

# Read Course by Code
def get_course(db: Session, course_code: str):
    course = db.query(Course).filter(Course.course_code == course_code, Course.is_deleted == False).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Read All Courses
def get_courses(db: Session):
    courses = db.query(Course).filter(Course.is_deleted == False).all()
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return courses
    
# Update Course
def update_course(db: Session, course_code: str, course_update: CourseUpdate):
    # Fetch the course by its code
    db_course = get_course(db, course_code)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check for unique constraints on course_code if it is being updated
    if course_update.course_code and course_update.course_code != db_course.course_code:
        existing_course = db.query(Course).filter(
            Course.course_code == course_update.course_code,
            Course.is_deleted == False
        ).first()
        if existing_course:
            raise HTTPException(status_code=400, detail="Course code already in use.")

    # Check if lecturer_id exists and update
    if course_update.lecturer_id:
        lecturer = db.query(Lecturer).filter(Lecturer.id == course_update.lecturer_id).first()
        if not lecturer:
            raise HTTPException(status_code=400, detail="Lecturer not found.")
        db_course.lecturer_id = course_update.lecturer_id
    
    # Update course_name if provided
    if course_update.course_name:
        db_course.course_name = course_update.course_name

    # Update course_code if provided
    if course_update.course_code:
        db_course.course_code = course_update.course_code
    
    # Commit the changes and refresh the course instance
    db.commit()
    db.refresh(db_course)
    
    return db_course


# Soft Delete Course
def delete_course(db: Session, course_code: str):
    db_course = get_course(db, course_code)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db_course.is_deleted = True
    db.commit()
    return {"message": "Course successfully deleted"}
