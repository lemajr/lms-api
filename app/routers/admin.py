from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import AdminCreate, AdminUpdate, AdminResponse
from app.crud.admin import create_admin, get_admin, get_admins, update_admin, delete_admin
from app.utils.dependency import get_db
from app.utils import oauth2

router = APIRouter()

# Create Admin
@router.post("/admin/", response_model=AdminResponse)
def create_admin_route(admin: AdminCreate, db: Session = Depends(get_db), get_current_user: AdminResponse = Depends(oauth2.get_current_user)):
    return create_admin(db, admin)

# Read Admin by ID
@router.get("/admin/{admin_id}", response_model=AdminResponse)
def read_admin(admin_id: str, db: Session = Depends(get_db),  get_current_user: AdminResponse = Depends(oauth2.get_current_user)):
    return get_admin(db, admin_id)

# Read All Admins
@router.get("/admins/", response_model=list[AdminResponse])
def read_admins(db: Session = Depends(get_db),  get_current_user: AdminResponse = Depends(oauth2.get_current_user)):
    return get_admins(db)

# Update Admin
@router.put("/admin/{admin_id}", response_model=AdminResponse)
def update_admin_route(admin_id: str, admin: AdminUpdate, db: Session = Depends(get_db),  get_current_user: AdminResponse = Depends(oauth2.get_current_user)):
    return update_admin(db, admin_id, admin)

# Delete Admin (Soft Delete)
@router.delete("/admin/{admin_id}")
def delete_admin_route(admin_id: str, db: Session = Depends(get_db),  get_current_user: AdminResponse = Depends(oauth2.get_current_user)):
    return delete_admin(db, admin_id)
