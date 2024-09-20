from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from sqlalchemy.exc import IntegrityError

# Create Course
def create_course(db: Session, course: CourseCreate):
    existing_course = db.query(Course).filter(
        Course.course_code == course.course_code,
        Course.is_deleted == False
    ).first()

    if existing_course:
        raise HTTPException(status_code=400, detail="Course with this course code already exists.")

    try:
        db_course = Course(
            course_name=course.course_name,
            course_code=course.course_code,
            description=course.description,
        )
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Course creation failed due to integrity issues.")

# Read Course by ID
def get_course(db: Session, course_code: str):
    course = db.query(Course).filter(Course.course_code == course_code, Course.is_deleted == False).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Read All Courses
def get_courses(db: Session):
    return db.query(Course).filter(Course.is_deleted == False).all()

# Update Course
def update_course(db: Session, course_code: str, course_update: CourseUpdate):
    db_course = get_course(db, course_code)
    if course_update.course_name:
        db_course.course_name = course_update.course_name
    if course_update.description:
        db_course.description = course_update.description
    
    db.commit()
    db.refresh(db_course)
    return db_course

# Soft Delete Course
def delete_course(db: Session, course_code: str):
    db_course = get_course(db, course_code)
    db_course.is_deleted = True
    db.commit()
    return {"message": "Course successfully deleted"}
