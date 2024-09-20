from sqlalchemy import Column, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.session import Base
import uuid

class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    course_code = Column(String, unique=True, nullable=False)  # Example: "COMP101"
    course_name = Column(String, nullable=False)               # Example: "Introduction to Programming"
    lecturer_id = Column(UUID(as_uuid=True), ForeignKey("lecturers.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    lecturer = relationship("Lecturer", back_populates="courses")
    students = relationship("Student", secondary="course_students", back_populates="courses")


class CourseStudent(Base):
    __tablename__ = "course_students"

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), primary_key=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), primary_key=True)
