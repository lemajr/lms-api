from sqlalchemy.orm import Session
from sqlalchemy import update

def soft_delete_entity(db: Session, model, entity_id: str):
    db.query(model).filter(model.id == entity_id).update({"is_deleted": True})
    db.commit()
