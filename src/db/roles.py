from sqlalchemy.orm import Session

from src.models.roles import Roles


def get_all_roles(db: Session):
    return db.query(Roles).all()


def create_role(role: Roles, db: Session):
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_role_by_id(role_id: str, db: Session):
    return db.query(Roles).filter(Roles.id == role_id).first()


def update_role(role: Roles, db: Session):
    db.commit()
    db.refresh(role)
    return role


def delete_role(role: Roles, db: Session):
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}


def get_roles_by_organization_id(organization_id: str, db: Session):
    return db.query(Roles).filter(Roles.organization_id == organization_id).all()
