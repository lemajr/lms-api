from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils.token import verify_token, create_access_token
from app.utils.dependency import get_db
from app.core import security
from app.models import user
from app.utils import oauth2

router = APIRouter()

# Student login
@router.post('/login')
def student_login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check if the user is a student
    student = db.query(user.Student).filter(
        user.Student.student_reg_no == request.username, 
        user.Student.is_active
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Student not found or inactive"
        )
    
    # Verify the password
    if not security.verify_password(request.password, student.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect password"
        )

    # Create access token for the student
    access_token = create_access_token(data={"sub": student.student_reg_no, "role": "student"})

    return {"access_token": access_token, "token_type": "bearer", "role": "student"}


# Staff login for lecturers and admins
@router.post('/staff-login')
def staff_login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check if the user is a lecturer
    lecturer = db.query(user.Lecturer).filter(
        user.Lecturer.lecturer_id == request.username, 
        user.Lecturer.is_active
    ).first()

    # If not a lecturer, check if it's an admin
    if not lecturer:
        admin = db.query(user.Admin).filter(
            user.Admin.admin_id == request.username, 
            user.Admin.is_active
        ).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Lecturer or Admin not found or inactive"
            )
        user_to_authenticate = admin
        role = "admin"
    else:
        user_to_authenticate = lecturer
        role = "lecturer"

    # Verify the password
    if not security.verify_password(request.password, user_to_authenticate.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect password"
        )

    # Create access token for the staff member
    access_token = create_access_token(data={"sub": user_to_authenticate.lecturer_id if role == "lecturer" else user_to_authenticate.admin_id, "role": role})

    return {"access_token": access_token, "token_type": "bearer", "role": role}


# Renew the access token
@router.post("/token/refresh")
async def refresh_token(token_str: str = Depends(oauth2.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Verify the token and extract token data
    token_data = verify_token(token_str, credentials_exception)

    # Create a new access token
    new_access_token = create_access_token(
        data={"sub": token_data.username, "role": token_data.role}
    )

    return {"access_token": new_access_token, "token_type": "bearer"}
