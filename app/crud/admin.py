from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import Admin
from app.schemas.user import AdminCreate, AdminUpdate
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError
from app.schemas.user import AdminResponse
from uuid import UUID

def create_admin(db: Session, admin: AdminCreate):
    # Check if admin with the same email or admin ID exists (excluding deleted ones)
    existing_admin = db.query(Admin).filter(
        (Admin.email == admin.email) | (Admin.admin_id == admin.admin_id),
        Admin.is_deleted == False
    ).first()

    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email or admin ID already exists.")

    # Create a new admin object
    db_admin = Admin(
        full_name=admin.full_name,
        email=admin.email,
        admin_id=admin.admin_id,
        password_hash=hash_password(admin.password),  # Ensure secure hashing
    )

    # Add to the database and commit the changes
    try:
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
    except IntegrityError as e:
        db.rollback()  # Roll back the session in case of an error
        raise HTTPException(status_code=400, detail="Admin with this email or admin ID already exists.")

    # Return the response using AdminResponse schema
    return AdminResponse.model_validate(db_admin)


# Read Admin by ID
def get_admin(db: Session, admin_id: UUID):
    admin = db.query(Admin).filter(Admin.id == admin_id, Admin.is_deleted == False).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

# Read All Admins
def get_admins(db: Session):
    db_all = db.query(Admin).filter(Admin.is_deleted == False).all()
    if not db_all:
            raise HTTPException(status_code=404, detail="No Admins found")
    return db_all

# Update Admin
def update_admin(db: Session, admin_id: UUID, admin_update: AdminUpdate):
    db_admin = get_admin(db, admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
     # Check for unique constraints
    if admin_update.email:
        existing_Admin = db.query(Admin).filter(
            Admin.email == admin_update.email,
            Admin.is_deleted == False
        ).first()
        if existing_Admin and existing_Admin.admin_id != admin_id:
            raise HTTPException(status_code=400, detail="Email already in use by another Admin.")

    if admin_update.admin_id:
        existing_Admin = db.query(Admin).filter(
            Admin.admin_id == admin_update.admin_id,
            Admin.is_deleted == False
        ).first()
        if existing_Admin and existing_Admin.admin_id != admin_id:
            raise HTTPException(status_code=400, detail="Admin ID already in use by another Admin.")
    
    if admin_update.full_name:
        db_admin.full_name = admin_update.full_name
    if admin_update.email:
        db_admin.email = admin_update.email
    if admin_update.password:
        db_admin.password_hash = hash_password(admin_update.password)
    
    db.commit()
    db.refresh(db_admin)
    return db_admin

# Soft Delete Admin
def delete_admin(db: Session, admin_id: str):
    db_admin = get_admin(db, admin_id)
    db_admin.is_deleted = True
    db.commit()
    return {"message": "Admin successfully deleted"}
