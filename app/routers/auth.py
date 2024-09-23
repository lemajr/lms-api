from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils import token
from app.utils.dependency import get_db
from app.core import security
from app.models import user

router = APIRouter()

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # First, check if the user is a student
    has_access = db.query(user.Student).filter(
        user.Student.student_reg_no == request.username, 
        user.Student.is_active
    ).first()

    # If not a student, check if it's a lecturer
    if not has_access:
        has_access = db.query(user.Lecturer).filter(
            user.Lecturer.lecturer_id == request.username, 
            user.Lecturer.is_active
        ).first()

    # If not a lecturer, check if it's an admin
    if not has_access:
        has_access = db.query(user.Admin).filter(
            user.Admin.admin_id == request.username, 
            user.Admin.is_active
        ).first()

    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found or inactive"
        )
    
    # Verify the password
    if not security.verify_password(request.password, has_access.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect password"
        )

    # Determine the role based on the user model type and use the right identifier
    if isinstance(has_access, user.Student):
        role = "student"
        identifier = has_access.student_reg_no
    elif isinstance(has_access, user.Lecturer):
        role = "lecturer"
        identifier = has_access.lecturer_id
    else:
        role = "admin"
        identifier = has_access.admin_id

    # Create access token with the correct identifier and role
    access_token = token.create_access_token(data={"sub": identifier, "role": role})

    return {"access_token": access_token, "token_type": "bearer", "role": role}
