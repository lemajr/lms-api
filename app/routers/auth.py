from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils.token import verify_token, create_access_token
from app.utils.dependency import get_db
from app.core import security
from app.models import user
from app.utils import oauth2
from app.schemas.user import AdminResponse, LecturerResponse, StudentResponse, UserResponse,TokenData

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
    access_token = create_access_token(data={"sub": identifier, "role": role})

    return {"access_token": access_token, "token_type": "bearer", "role": role}

# Renew the access token
@router.post("/token/refresh")
async def refresh_token(token_str: str = Depends(oauth2.oauth2_scheme)):
    # Use the exception handling logic from get_current_user for consistency
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Verify the token and get token data
    token_data = verify_token(token_str, credentials_exception)

    # Create a new access token using the token data
    new_access_token = create_access_token(
        data={"sub": token_data.username, "role": token_data.role}
    )

    return {"access_token": new_access_token, "token_type": "bearer"}



# # user profile
# @router.get("/me", response_model=UserResponse)
# def get_current_user_info(db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
#     print(f"Current User: {current_user}")

#     if not current_user:
#         raise HTTPException(status_code=401, detail="Not authenticated")

#     user_data = None
#     user_response_data = None

#     # Fetch user details based on their role
#     if current_user.role == "student":
#         user_data = db.query(user.Student).filter(user.Student.student_reg_no == current_user.username).first()
#         if user_data:
#             user_response_data = StudentResponse.model_validate(user_data)
#     elif current_user.role == "lecturer":
#         user_data = db.query(user.Lecturer).filter(user.Lecturer.lecturer_id == current_user.username).first()
#         if user_data:
#             user_response_data = LecturerResponse.model_validate(user_data)
#     elif current_user.role == "admin":
#         user_data = db.query(user.Admin).filter(user.Admin.admin_id == current_user.username).first()
#         if user_data:
#             user_response_data = AdminResponse.model_validate(user_data)
#     else:
#         raise HTTPException(status_code=400, detail="Invalid role")

#     if not user_data:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Use 'id' instead of 'uuid' here
#     return UserResponse(
#         id=user_data.id,  # Access the 'id' field instead of 'uuid'
#         full_name=user_data.full_name,
#         email=user_data.email,
#         role=current_user.role,
#         created_at=user_data.created_at,
#         updated_at=user_data.updated_at,
#         is_active=user_data.is_active,
#         is_deleted=user_data.is_deleted,
#         user_data=user_response_data  # Nested student, lecturer, or admin data
#     )
