from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.roles import (
    create_role as repo_create_role,
    delete_role as repo_delete_role,
    get_all_roles as repo_get_all_roles,
    get_role_by_id as repo_get_role_by_id,
    get_roles_by_organization_id as repo_get_roles_by_organization_id,
    update_role as repo_update_role,
)
from src.dtos.roles import RoleCreateDTO
from src.models.roles import Roles
from src.utils.constants import ROLE_NOT_FOUND, ROLES_NOT_FOUND_FOR_ORGANIZATION


def get_all_roles(db: Session):
    return repo_get_all_roles(db)


def add_role(role: RoleCreateDTO, db: Session):
    data = role.model_dump()
    new_role = Roles(**data)
    return repo_create_role(new_role, db)


def get_role_by_id(role_id: str, db: Session):
    role = repo_get_role_by_id(role_id, db)
    if role is None:
        raise HTTPException(status_code=404, detail=ROLE_NOT_FOUND)
    return role


def delete_role_by_id(role_id: str, db: Session):
    role = repo_get_role_by_id(role_id, db)
    if role is None:
        raise HTTPException(status_code=404, detail=ROLE_NOT_FOUND)
    return repo_delete_role(role, db)


def update_role_by_id(role_id: str, role: RoleCreateDTO, db: Session):
    existing_role = repo_get_role_by_id(role_id, db)
    if existing_role is None:
        raise HTTPException(status_code=404, detail=ROLE_NOT_FOUND)
    existing_role.name = role.name
    existing_role.description = role.description
    existing_role.organization_id = role.organization_id
    existing_role.active = role.active
    return repo_update_role(existing_role, db)


def get_organization_roles_by_id(organization_id: str, db: Session):
    roles = repo_get_roles_by_organization_id(organization_id, db)
    if roles is None:
        raise HTTPException(status_code=404, detail=ROLES_NOT_FOUND_FOR_ORGANIZATION)
    return roles
