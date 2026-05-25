from fastapi import APIRouter, Depends;

from ..controllers.roles import (
    add_role,
    delete_role_by_id,
    get_all_roles,
    get_role_by_id,
    update_role_by_id,
    get_organization_roles_by_id,
);
from ..dtos.roles import RoleCreateDTO, RoleDTO;
from ..utils.db import get_db;

router = APIRouter(prefix="/roles", tags=["Roles"]);


@router.get("/", response_model=list[RoleDTO])
def get_roles(db=Depends(get_db)):
    return get_all_roles(db);


@router.get("/{role_id}", response_model=RoleDTO)
def role_by_id(role_id: str, db=Depends(get_db)):
    return get_role_by_id(role_id, db);


@router.post("/", response_model=RoleDTO)
def create_role(data: RoleCreateDTO, db=Depends(get_db)):
    return add_role(data, db);


@router.put("/{role_id}", response_model=RoleDTO)
def update_role(role_id: str, data: RoleCreateDTO, db=Depends(get_db)):
    return update_role_by_id(role_id, data, db);


@router.delete("/{role_id}", response_model=dict)
def delete_role(role_id: str, db=Depends(get_db)):
    return delete_role_by_id(role_id, db);

@router.get("/organization/{organization_id}", response_model=list[RoleDTO])
def get_organization_roles(organization_id: str, db=Depends(get_db)):
    return get_organization_roles_by_id(organization_id, db);