from fastapi import HTTPException;
from sqlalchemy.orm import Session;

from src.dtos.roles import RoleCreateDTO;
from src.models.roles import Roles;
from src.utils.constants import ROLE_NOT_FOUND, ROLES_NOT_FOUND_FOR_ORGANIZATION;


def get_all_roles(db: Session):
    return db.query(Roles).all();


def add_role(role: RoleCreateDTO, db: Session):
    data = role.model_dump();
    new_role = Roles(**data);
    db.add(new_role);
    db.commit();
    db.refresh(new_role);
    return new_role;


def get_role_by_id(role_id: str, db: Session):
    role = db.query(Roles).filter(Roles.id == role_id).first();
    if role is None:
        raise HTTPException(status_code=404, detail=ROLE_NOT_FOUND);
    return role;


def delete_role_by_id(role_id: str, db: Session):
    role = db.query(Roles).filter(Roles.id == role_id).first();
    if role is None:
        raise HTTPException(status_code=404, detail=ROLE_NOT_FOUND);
    db.delete(role);
    db.commit();
    return {"message": "Role deleted successfully"};


def update_role_by_id(role_id: str, role: RoleCreateDTO, db: Session):
    existing_role = db.query(Roles).filter(Roles.id == role_id).first();
    if existing_role is None:
        raise HTTPException(status_code=404, detail=ROLE_NOT_FOUND);
    existing_role.name = role.name;
    existing_role.description = role.description;
    existing_role.organization_id = role.organization_id;
    existing_role.active = role.active;
    db.commit();
    db.refresh(existing_role);
    return existing_role;

def get_organization_roles_by_id(organization_id: str, db: Session):
    roles = db.query(Roles).filter(Roles.organization_id == organization_id).all();
    if roles is None:
        raise HTTPException(status_code=404, detail=ROLES_NOT_FOUND_FOR_ORGANIZATION);
    return roles;