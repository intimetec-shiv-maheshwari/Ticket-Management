from fastapi import APIRouter, Depends;

from ..services.users import (
    add_user,
    delete_user_by_id,
    get_all_users,
    get_user_by_id,
    login_user,
    update_user_by_id,
    get_users_by_organization_id,
);
from ..dtos.users import UserCreateDTO, UserDTO, UserLoginDTO;
from ..utils.db import get_db;

router = APIRouter(prefix="/users", tags=["Users"]);


@router.get("/", response_model=list[UserDTO])
def get_users(db=Depends(get_db)):
    return get_all_users(db);


@router.post("/login", response_model=UserDTO)
def login(data: UserLoginDTO, db=Depends(get_db)):
    return login_user(data, db);


@router.get("/{user_id}", response_model=UserDTO)
def user_by_id(user_id: str, db=Depends(get_db)):
    return get_user_by_id(user_id, db);


@router.post("/", response_model=UserDTO)
def create_user(data: UserCreateDTO, db=Depends(get_db)):
    return add_user(data, db);


@router.put("/{user_id}", response_model=UserDTO)
def update_user(user_id: str, data: UserCreateDTO, db=Depends(get_db)):
    return update_user_by_id(user_id, data, db);


@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: str, db=Depends(get_db)):
    return delete_user_by_id(user_id, db);

@router.get("/organization/{organization_id}", response_model=list[UserDTO])
def get_organization_users(organization_id: str, db=Depends(get_db)):
    return get_users_by_organization_id(organization_id, db);
