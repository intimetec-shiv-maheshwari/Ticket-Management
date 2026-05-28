from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.users import (
    create_user as repo_create_user,
    delete_user as repo_delete_user,
    get_all_users as repo_get_all_users,
    get_user_by_email,
    get_user_by_id as repo_get_user_by_id,
    get_users_by_organization_id as repo_get_users_by_organization_id,
    update_user as repo_update_user,
)
from src.dtos.users import UserCreateDTO, UserLoginDTO
from src.models.users import Users
from src.utils.constants import (
    INVALID_CREDENTIALS,
    USER_INACTIVE,
    USER_NOT_FOUND,
    USERS_NOT_FOUND_FOR_ORGANIZATION,
)


def get_all_users(db: Session):
    return repo_get_all_users(db)


def add_user(user: UserCreateDTO, db: Session):
    data = user.model_dump()
    new_user = Users(**data)
    return repo_create_user(new_user, db)


def login_user(credentials: UserLoginDTO, db: Session):
    user = get_user_by_email(credentials.email, db)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=401, detail=INVALID_CREDENTIALS)
    if not user.active:
        raise HTTPException(status_code=403, detail=USER_INACTIVE)
    return user


def get_user_by_id(user_id: str, db: Session):
    user = repo_get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return user


def delete_user_by_id(user_id: str, db: Session):
    user = repo_get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return repo_delete_user(user, db)


def update_user_by_id(user_id: str, user: UserCreateDTO, db: Session):
    existing_user = repo_get_user_by_id(user_id, db)
    if existing_user is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.password = user.password
    existing_user.organization_id = user.organization_id
    existing_user.role_id = user.role_id
    existing_user.active = user.active
    return repo_update_user(existing_user, db)


def get_users_by_organization_id(organization_id: str, db: Session):
    users = repo_get_users_by_organization_id(organization_id, db)
    if users is None:
        raise HTTPException(status_code=404, detail=USERS_NOT_FOUND_FOR_ORGANIZATION)
    return users
